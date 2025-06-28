import re
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.database_models import (
    Product, Inventory, InboundShipment, InboundItem, 
    OutboundOrder, OutboundItem, Vendor, Customer, ChatMessage
)
from .inventory_service import InventoryService
from .inbound_service import InboundService
from .outbound_service import OutboundService

class ChatbotService:
    def __init__(self, db: Session):
        self.db = db
        self.inventory_service = InventoryService(db)
        self.inbound_service = InboundService(db)
        self.outbound_service = OutboundService(db)

    def process_message(self, user_message: str, session_id: str = "default", user_id: str = "anonymous") -> Dict:
        """Process user message and return appropriate response"""
        user_message = user_message.strip().lower()
        
        # Determine intent
        intent, confidence = self._classify_intent(user_message)
        
        # Process based on intent
        response_data = self._process_intent(intent, user_message)
        
        # Save chat message
        chat_message = ChatMessage(
            user_message=user_message,
            bot_response=response_data["message"],
            intent=intent,
            action_taken=response_data.get("action_taken", ""),
            success=response_data.get("success", True),
            session_id=session_id,
            user_id=user_id
        )
        self.db.add(chat_message)
        self.db.commit()
        
        return {
            "message": response_data["message"],
            "intent": intent,
            "data": response_data.get("data"),
            "actions": response_data.get("actions", []),
            "success": response_data.get("success", True)
        }

    def _classify_intent(self, message: str) -> Tuple[str, float]:
        """Classify user intent based on keywords and patterns"""
        message = message.lower()
        
        # Intent patterns
        intent_patterns = {
            "inventory_check": [
                r"check\s+(stock|inventory)", r"how\s+much\s+.+\s+stock",
                r"available\s+quantity", r"stock\s+level", r"inventory\s+status"
            ],
            "inbound_gate_in": [
                r"gate\s+in", r"receiving\s+delivery", r"delivery\s+arrived",
                r"shipment\s+arrived", r"vendor\s+delivery", r"inbound\s+delivery"
            ],
            "outbound_dispatch": [
                r"dispatch", r"ship\s+order", r"send\s+out", r"outbound",
                r"delivery\s+ready", r"pick\s+and\s+pack"
            ],
            "stock_update": [
                r"update\s+stock", r"add\s+inventory", r"received\s+\d+",
                r"stock\s+adjustment", r"manual\s+update", r"add\s+\d+",
                r"add\s+\d+\s+units"
            ],
            "order_status": [
                r"order\s+status", r"check\s+order", r"order\s+\w+",
                r"shipment\s+status", r"delivery\s+status"
            ],
            "low_stock_alert": [
                r"low\s+stock", r"reorder\s+alert", r"stock\s+alert",
                r"minimum\s+stock", r"needs\s+reorder"
            ],
            "help": [
                r"help", r"what\s+can\s+you\s+do", r"commands", r"how\s+to"
            ]
        }
        
        best_intent = "general"
        best_confidence = 0.0
        
        for intent, patterns in intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    confidence = 0.8  # Base confidence for pattern match
                    if confidence > best_confidence:
                        best_intent = intent
                        best_confidence = confidence
        
        return best_intent, best_confidence

    def _process_intent(self, intent: str, message: str) -> Dict:
        """Process specific intent and return response"""
        try:
            if intent == "inventory_check":
                return self._handle_inventory_check(message)
            elif intent == "inbound_gate_in":
                return self._handle_inbound_gate_in(message)
            elif intent == "outbound_dispatch":
                return self._handle_outbound_dispatch(message)
            elif intent == "stock_update":
                return self._handle_stock_update(message)
            elif intent == "order_status":
                return self._handle_order_status(message)
            elif intent == "low_stock_alert":
                return self._handle_low_stock_alert(message)
            elif intent == "help":
                return self._handle_help()
            else:
                return self._handle_general(message)
        except Exception as e:
            return {
                "message": f"Sorry, I encountered an error: {str(e)}",
                "success": False,
                "action_taken": "error_occurred"
            }

    def _handle_inventory_check(self, message: str) -> Dict:
        """Handle inventory check requests"""
        # Try to extract SKU or product name
        sku_match = re.search(r"(sku|SKU)\s*:?\s*(\w+)", message)
        if sku_match:
            sku = sku_match.group(2).upper()  # Convert to uppercase for consistency
            product = self.inventory_service.get_product_by_sku(sku)
            if product:
                inventory = self.db.query(Inventory).filter(Inventory.product_id == product.id).first()
                return {
                    "message": f"**{product.name}** (SKU: {product.sku})\n"
                              f"Available: {inventory.available_quantity} {product.unit}\n"
                              f"Reserved: {inventory.reserved_quantity} {product.unit}\n"
                              f"Total: {inventory.quantity} {product.unit}\n"
                              f"Location: {product.location or 'Not set'}",
                    "data": {
                        "product": product.name,
                        "sku": product.sku,
                        "available": inventory.available_quantity,
                        "reserved": inventory.reserved_quantity,
                        "total": inventory.quantity
                    },
                    "success": True,
                    "action_taken": f"inventory_check_for_{sku}"
                }
            else:
                return {
                    "message": f"Product with SKU '{sku}' not found.",
                    "success": False,
                    "action_taken": f"inventory_check_failed_{sku}"
                }
        else:
            # Return general inventory summary
            summary = self.inventory_service.get_inventory_summary()
            return {
                "message": f"**Inventory Summary**\n"
                          f"Total Products: {summary['total_products']}\n"
                          f"Low Stock Items: {summary['low_stock_count']}\n\n"
                          f"To check specific product, use: 'Check stock SKU: PRODUCT_SKU'",
                "data": summary,
                "success": True,
                "action_taken": "inventory_summary_provided"
            }

    def _handle_inbound_gate_in(self, message: str) -> Dict:
        """Handle inbound gate-in requests"""
        # Extract shipment details
        shipment_match = re.search(r"shipment\s+(\w+)", message)
        quantity_match = re.search(r"(\d+)\s*(\w+)?", message)
        
        if shipment_match:
            shipment_number = shipment_match.group(1).upper()  # Convert to uppercase for consistency
            shipment = self.inbound_service.get_shipment_by_number(shipment_number)
            
            if shipment:
                # Update shipment status to arrived
                self.inbound_service.update_shipment_status(shipment.id, "arrived")
                
                return {
                    "message": f" **Shipment {shipment_number} Gate-In Complete**\n"
                              f"Vendor: {shipment.vendor.name}\n"
                              f"Status: Arrived\n"
                              f"Next: Please proceed with quality check and stock update.",
                    "data": {"shipment_id": shipment.id, "shipment_number": shipment_number},
                    "actions": ["quality_check", "stock_update"],
                    "success": True,
                    "action_taken": f"gate_in_completed_{shipment_number}"
                }
            else:
                return {
                    "message": f" Shipment '{shipment_number}' not found. Please check the shipment number.",
                    "success": False,
                    "action_taken": f"gate_in_failed_{shipment_number}"
                }
        else:
            return {
                "message": "To process gate-in, please provide shipment details:\n"
                          "Example: 'Gate in shipment SH001'\n"
                          "Or: 'Delivery arrived for shipment SH001'",
                "success": True,
                "action_taken": "gate_in_help_provided"
            }

    def _handle_outbound_dispatch(self, message: str) -> Dict:
        """Handle outbound dispatch requests"""
        order_match = re.search(r"order\s+(\w+)", message)
        
        if order_match:
            order_number = order_match.group(1).upper()  # Convert to uppercase for consistency
            order = self.outbound_service.get_order_by_number(order_number)
            
            if order:
                # Update order status to dispatched
                success = self.outbound_service.update_order_status(order.id, "dispatched")
                
                if success:
                    return {
                        "message": f" **Order {order_number} Dispatched**\n"
                                  f"Customer: {order.customer.name}\n"
                                  f"Items: {len(order.items)} products\n"
                                  f"Status: Dispatched\n"
                                  f"Customer notification sent!",
                        "data": {"order_id": order.id, "order_number": order_number},
                        "success": True,
                        "action_taken": f"dispatch_completed_{order_number}"
                    }
                else:
                    return {
                        "message": f" Failed to dispatch order {order_number}. Please check order status.",
                        "success": False,
                        "action_taken": f"dispatch_failed_{order_number}"
                    }
            else:
                return {
                    "message": f" Order '{order_number}' not found. Please check the order number.",
                    "success": False,
                    "action_taken": f"dispatch_order_not_found_{order_number}"
                }
        else:
            return {
                "message": "To dispatch an order, please provide order details:\n"
                          "Example: 'Dispatch order ORD001'\n"
                          "Or: 'Ship order ORD001'",
                "success": True,
                "action_taken": "dispatch_help_provided"
            }

    def _handle_stock_update(self, message: str) -> Dict:
        """Handle manual stock updates"""
        # Extract SKU and quantity
        sku_match = re.search(r"(sku|SKU)\s*:?\s*(\w+)", message)
        quantity_match = re.search(r"(\d+)\s*(\w+)?", message)
        
        if sku_match and quantity_match:
            sku = sku_match.group(2).upper()  # Convert to uppercase for consistency
            quantity = int(quantity_match.group(1))
            
            product = self.inventory_service.get_product_by_sku(sku)
            if product:
                # Determine if it's addition or adjustment
                if "add" in message or "receive" in message:
                    success = self.inventory_service.update_stock(
                        product.id, quantity, "adjustment", 
                        reason="Manual addition via chatbot"
                    )
                    operation = "added"
                else:
                    success = self.inventory_service.update_stock(
                        product.id, quantity, "adjustment",
                        reason="Manual update via chatbot"
                    )
                    operation = "updated"
                
                if success:
                    return {
                        "message": f" **Stock {operation}**\n"
                                  f"Product: {product.name}\n"
                                  f"SKU: {sku}\n"
                                  f"Quantity {operation}: {quantity}\n"
                                  f"Stock updated successfully!",
                        "data": {"sku": sku, "quantity": quantity, "operation": operation},
                        "success": True,
                        "action_taken": f"stock_{operation}_{sku}_{quantity}"
                    }
                else:
                    return {
                        "message": f" Failed to update stock for {sku}. Please try again.",
                        "success": False,
                        "action_taken": f"stock_update_failed_{sku}"
                    }
            else:
                return {
                    "message": f" Product with SKU '{sku}' not found.",
                    "success": False,
                    "action_taken": f"stock_update_product_not_found_{sku}"
                }
        else:
            return {
                "message": "To update stock, please provide SKU and quantity:\n"
                          "Example: 'Add 50 units SKU: PROD001'\n"
                          "Or: 'Update stock SKU: PROD001 quantity 25'",
                "success": True,
                "action_taken": "stock_update_help_provided"
            }

    def _handle_order_status(self, message: str) -> Dict:
        """Handle order status requests"""
        # Look for patterns like "order ORD001" or "check order ORD001" or "status ORD001"
        order_match = re.search(r"(?:order|status)\s+(\w+)", message)
        
        if order_match:
            order_number = order_match.group(1).upper()  # Convert to uppercase for consistency
            order = self.outbound_service.get_order_by_number(order_number)
            
            if order:
                return {
                    "message": f" **Order Status: {order_number}**\n"
                              f"Customer: {order.customer.name}\n"
                              f"Status: {order.status.title()}\n"
                              f"Order Date: {order.order_date.strftime('%Y-%m-%d')}\n"
                              f"Items: {len(order.items)} products",
                    "data": {
                        "order_number": order_number,
                        "status": order.status,
                        "customer": order.customer.name,
                        "items_count": len(order.items)
                    },
                    "success": True,
                    "action_taken": f"order_status_checked_{order_number}"
                }
            else:
                return {
                    "message": f" Order '{order_number}' not found.",
                    "success": False,
                    "action_taken": f"order_status_not_found_{order_number}"
                }
        else:
            return {
                "message": "To check order status, please provide order number:\n"
                          "Example: 'Check order ORD001'\n"
                          "Or: 'Order status ORD001'",
                "success": True,
                "action_taken": "order_status_help_provided"
            }

    def _handle_low_stock_alert(self, message: str) -> Dict:
        """Handle low stock alert requests"""
        summary = self.inventory_service.get_inventory_summary()
        low_stock_items = summary["low_stock_alerts"]
        
        if low_stock_items:
            message_text = " **Low Stock Alert**\n\n"
            for item in low_stock_items[:5]:  # Show top 5
                message_text += f" {item['name']} (SKU: {item['sku']})\n"
                message_text += f"  Available: {item['available_quantity']} | Reorder Level: {item['reorder_level']}\n\n"
            
            if len(low_stock_items) > 5:
                message_text += f"... and {len(low_stock_items) - 5} more items need attention."
        else:
            message_text = " **All stock levels are healthy!**\nNo items are currently below reorder level."
        
        return {
            "message": message_text,
            "data": {"low_stock_items": low_stock_items, "count": len(low_stock_items)},
            "success": True,
            "action_taken": "low_stock_alert_checked"
        }

    def _handle_help(self) -> Dict:
        """Handle help requests"""
        help_text = """
 **Smart Warehouse Assistant Help**

I can help you with:

 **Inventory Management:**
 "Check stock SKU: PROD001"
 "Inventory summary"
 "Low stock alerts"

 **Inbound Operations:**
 "Gate in shipment SH001"
 "Delivery arrived for shipment SH001"

 **Outbound Operations:**
 "Dispatch order ORD001"
 "Check order status ORD001"

 **Stock Updates:**
 "Add 50 units SKU: PROD001"
 "Update stock SKU: PROD001 quantity 25"

Just type your request in natural language, and I'll help you manage your warehouse operations!
        """
        
        return {
            "message": help_text.strip(),
            "success": True,
            "action_taken": "help_provided"
        }

    def _handle_general(self, message: str) -> Dict:
        """Handle general messages"""
        return {
            "message": "I'm here to help with warehouse operations! "
                      "Try asking about inventory, orders, or shipments. "
                      "Type 'help' to see what I can do.",
            "success": True,
            "action_taken": "general_response_provided"
        }
