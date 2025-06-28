from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    unit = Column(String(50), default="pcs")  # pieces, kg, liters, etc.
    unit_price = Column(Float, default=0.0)
    reorder_level = Column(Integer, default=10)
    location = Column(String(100))  # warehouse location/zone
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    inventory_items = relationship("Inventory", back_populates="product")
    inbound_items = relationship("InboundItem", back_populates="product")
    outbound_items = relationship("OutboundItem", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)  # reserved for outbound orders
    available_quantity = Column(Integer, default=0)  # quantity - reserved_quantity
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="inventory_items")

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    inbound_shipments = relationship("InboundShipment", back_populates="vendor")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    outbound_orders = relationship("OutboundOrder", back_populates="customer")

class InboundShipment(Base):
    __tablename__ = "inbound_shipments"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_number = Column(String(100), unique=True, nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    expected_date = Column(DateTime)
    actual_arrival_date = Column(DateTime)
    status = Column(String(50), default="pending")  # pending, arrived, checked_in, completed
    driver_name = Column(String(100))
    vehicle_number = Column(String(50))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vendor = relationship("Vendor", back_populates="inbound_shipments")
    items = relationship("InboundItem", back_populates="shipment")

class InboundItem(Base):
    __tablename__ = "inbound_items"
    
    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("inbound_shipments.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    expected_quantity = Column(Integer, nullable=False)
    received_quantity = Column(Integer, default=0)
    damaged_quantity = Column(Integer, default=0)
    unit_cost = Column(Float, default=0.0)
    batch_number = Column(String(100))
    expiry_date = Column(DateTime)
    notes = Column(Text)
    
    # Relationships
    shipment = relationship("InboundShipment", back_populates="items")
    product = relationship("Product", back_populates="inbound_items")

class OutboundOrder(Base):
    __tablename__ = "outbound_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_dispatch_date = Column(DateTime)
    actual_dispatch_date = Column(DateTime)
    status = Column(String(50), default="pending")  # pending, picking, packed, dispatched, delivered
    priority = Column(String(20), default="normal")  # low, normal, high, urgent
    delivery_address = Column(Text)
    tracking_number = Column(String(100))
    vehicle_number = Column(String(50))
    driver_name = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="outbound_orders")
    items = relationship("OutboundItem", back_populates="order")

class OutboundItem(Base):
    __tablename__ = "outbound_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("outbound_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    ordered_quantity = Column(Integer, nullable=False)
    picked_quantity = Column(Integer, default=0)
    packed_quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0.0)
    notes = Column(Text)
    
    # Relationships
    order = relationship("OutboundOrder", back_populates="items")
    product = relationship("Product", back_populates="outbound_items")

class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(String(50), nullable=False)  # inbound, outbound, adjustment, transfer
    quantity = Column(Integer, nullable=False)  # positive for inbound, negative for outbound
    reference_type = Column(String(50))  # inbound_shipment, outbound_order, adjustment, transfer
    reference_id = Column(Integer)  # ID of the reference record
    reason = Column(String(200))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))  # user who created the movement
    
    # Relationships
    product = relationship("Product")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(200))
    role = Column(String(50), default="operator")  # admin, supervisor, operator, viewer
    department = Column(String(100))  # inbound, outbound, inventory, management
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    preferences = Column(JSON)  # User preferences for chatbot behavior
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chat_sessions = relationship("ChatSession", back_populates="user")
    chat_messages = relationship("ChatMessage", back_populates="user")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200))  # Auto-generated session title based on first query
    context_summary = Column(Text)  # Summary of conversation context
    is_active = Column(Boolean, default=True)
    total_messages = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")
    context_entries = relationship("ConversationContext", back_populates="session")

class ConversationContext(Base):
    __tablename__ = "conversation_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    context_type = Column(String(50), nullable=False)  # user_info, warehouse_state, ongoing_task, entity_reference
    context_key = Column(String(100), nullable=False)  # e.g., "current_product", "active_shipment", "user_preference"
    context_value = Column(JSON, nullable=False)  # Flexible JSON storage for context data
    relevance_score = Column(Float, default=1.0)  # How relevant this context is (decays over time)
    expires_at = Column(DateTime)  # When this context should expire
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="context_entries")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    intent = Column(String(100))  # inbound, outbound, inventory_check, etc.
    confidence_score = Column(Float)  # LLM confidence in the response
    action_taken = Column(String(200))  # description of action performed
    context_used = Column(JSON)  # Context that was used for this response
    feedback_score = Column(Integer)  # User feedback (1-5 stars)
    feedback_text = Column(Text)  # User feedback text
    processing_time = Column(Float)  # Time taken to generate response (seconds)
    enhanced_mode = Column(Boolean, default=False)  # Whether LLM was used
    success = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    user = relationship("User", back_populates="chat_messages")

# Phase 3: Forecasting and Space Planning Models

class SalesHistory(Base):
    __tablename__ = "sales_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(DateTime, nullable=False)
    unit_price = Column(Float, default=0.0)
    total_value = Column(Float, default=0.0)
    customer_type = Column(String(50))  # retail, wholesale, b2b
    season = Column(String(20))  # Q1, Q2, Q3, Q4 or Winter, Spring, Summer, Fall
    channel = Column(String(50))  # online, store, b2b
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])

class DemandForecast(Base):
    __tablename__ = "demand_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    forecast_date = Column(DateTime, nullable=False)  # Week/month being forecasted
    predicted_demand = Column(Integer, nullable=False)
    confidence_level = Column(Float, default=0.0)  # 0-1 confidence score
    forecast_type = Column(String(20), default="weekly")  # weekly, monthly
    seasonal_factor = Column(Float, default=1.0)
    trend_factor = Column(Float, default=1.0)
    ai_generated = Column(Boolean, default=True)
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])

class StockAlert(Base):
    __tablename__ = "stock_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)  # overstock, understock, reorder
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    current_stock = Column(Integer, nullable=False)
    recommended_stock = Column(Integer)
    predicted_stockout_date = Column(DateTime)
    reorder_quantity = Column(Integer)
    reorder_urgency = Column(String(20), default="normal")  # urgent, normal, low
    ai_generated = Column(Boolean, default=True)
    message = Column(Text)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])

class WarehouseLayout(Base):
    __tablename__ = "warehouse_layouts"
    
    id = Column(Integer, primary_key=True, index=True)
    zone_code = Column(String(20), nullable=False)  # A1, A2, B1, etc.
    zone_name = Column(String(100))
    zone_type = Column(String(50))  # receiving, storage, picking, dispatch
    capacity = Column(Integer, default=0)  # maximum items
    current_utilization = Column(Integer, default=0)  # current items
    utilization_percentage = Column(Float, default=0.0)
    distance_from_entrance = Column(Float, default=0.0)  # meters
    distance_from_exit = Column(Float, default=0.0)  # meters
    accessibility_score = Column(Float, default=1.0)  # 0-1 how accessible
    preferred_categories = Column(JSON)  # list of preferred product categories
    temperature_zone = Column(String(20), default="ambient")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SpaceOptimization(Base):
    __tablename__ = "space_optimizations"
    
    id = Column(Integer, primary_key=True, index=True)
    optimization_type = Column(String(50), nullable=False)  # layout, category_grouping, velocity_based
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(String(20), default="medium")  # low, medium, high
    expected_benefit = Column(Text)
    implementation_effort = Column(String(20), default="medium")  # low, medium, high
    affected_products = Column(JSON)  # list of product IDs
    affected_zones = Column(JSON)  # list of zone codes
    ai_generated = Column(Boolean, default=True)
    status = Column(String(20), default="pending")  # pending, approved, implemented, rejected
    implemented_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProductVelocity(Base):
    __tablename__ = "product_velocities"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    velocity_category = Column(String(20), nullable=False)  # fast, medium, slow, dead
    weekly_turnover = Column(Float, default=0.0)  # units per week
    monthly_turnover = Column(Float, default=0.0)  # units per month
    days_of_supply = Column(Integer, default=0)  # how many days current stock will last
    pick_frequency = Column(Integer, default=0)  # picks per period
    last_movement_date = Column(DateTime)
    movement_trend = Column(String(20), default="stable")  # increasing, decreasing, stable, volatile
    seasonality_pattern = Column(JSON)  # seasonal movement patterns
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", foreign_keys=[product_id])
