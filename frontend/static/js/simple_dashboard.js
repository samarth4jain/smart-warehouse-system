// Simplified Dashboard JavaScript - Focus on Data Display
console.log('🚀 Simplified Dashboard v2.0 loaded');

class SimpleDashboard {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8001';
        this.init();
    }
    
    async init() {
        console.log('🔧 Initializing dashboard...');
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.loadData());
        } else {
            await this.loadData();
        }
        
        // Auto-refresh every 30 seconds
        setInterval(() => this.loadData(), 30000);
    }
    
    async loadData() {
        console.log('📊 Loading dashboard data...');
        
        try {
            // Load both overview and recent activity
            const [overviewResponse, activityResponse] = await Promise.all([
                fetch(`${this.apiBaseUrl}/api/dashboard/overview`),
                fetch(`${this.apiBaseUrl}/api/dashboard/recent-activity`)
            ]);
            
            if (!overviewResponse.ok || !activityResponse.ok) {
                throw new Error(`API Error: ${overviewResponse.status || activityResponse.status}`);
            }
            
            const overviewData = await overviewResponse.json();
            const activityData = await activityResponse.json();
            
            console.log('✅ Overview data received:', overviewData);
            console.log('✅ Activity data received:', activityData);
            
            this.updateMetrics(overviewData);
            this.updateActivity(activityData);
            
        } catch (error) {
            console.error('❌ Error loading data:', error);
            this.showStatus(`❌ Error: ${error.message}`, 'error');
        }
    }
    
    updateMetrics(data) {
        console.log('🎯 Updating metrics...');
        
        const updates = [
            { id: 'total-products', value: data.inventory.total_products },
            { id: 'low-stock-items', value: data.inventory.low_stock_items },
            { id: 'pending-inbound', value: data.operations.pending_inbound },
            { id: 'pending-outbound', value: data.operations.pending_outbound }
        ];
        
        updates.forEach(({ id, value }) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
                console.log(`✅ Updated ${id}: ${value}`);
            } else {
                console.warn(`⚠️ Element not found: ${id}`);
            }
        });
    }
    
    updateActivity(data) {
        console.log('📈 Updating recent activity...');
        
        const activityContainer = document.getElementById('activity-container');
        if (!activityContainer) {
            console.warn('⚠️ Activity container not found');
            return;
        }
        
        if (!data.activities || data.activities.length === 0) {
            activityContainer.innerHTML = '<p class="no-activity">No recent activity</p>';
            return;
        }
        
        const activityHTML = data.activities.map(activity => {
            const time = new Date(activity.timestamp).toLocaleString();
            const typeIcon = this.getActivityIcon(activity.type);
            const typeClass = activity.details?.movement_type || activity.type;
            
            return `
                <div class="activity-item ${typeClass}">
                    <div class="activity-icon">
                        <i class="fas ${typeIcon}"></i>
                    </div>
                    <div class="activity-content">
                        <p class="activity-description">${activity.description}</p>
                        <span class="activity-time">${time}</span>
                    </div>
                </div>
            `;
        }).join('');
        
        activityContainer.innerHTML = activityHTML;
        console.log(`✅ Updated activity: ${data.activities.length} items`);
    }
    
    getActivityIcon(type) {
        const icons = {
            'stock_movement': 'fa-boxes',
            'inbound': 'fa-truck',
            'outbound': 'fa-shipping-fast',
            'inventory_update': 'fa-edit',
            'system': 'fa-cog'
        };
        return icons[type] || 'fa-circle';
    }
    
    showStatus(message, type) {
        console.log(`📢 Status: ${message}`);
        
        // Try to show status in UI if there's a status element
        const statusEl = document.getElementById('dashboard-status');
        if (statusEl) {
            statusEl.textContent = message;
            statusEl.className = `status ${type}`;
        }
    }
}

// Initialize when script loads
const dashboard = new SimpleDashboard();

// Global functions for manual testing
window.reloadDashboard = () => dashboard.loadData();
window.dashboard = dashboard;

// Navigation functionality
function showSection(sectionName) {
    console.log('🔄 Switching to section:', sectionName);
    
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Show the selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Update active navigation item
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Find and activate the correct nav item
    const activeNavItem = document.querySelector(`[onclick="showSection('${sectionName}')"]`)?.closest('.nav-item');
    if (activeNavItem) {
        activeNavItem.classList.add('active');
    }
    
    // Update page title
    const pageTitle = document.getElementById('page-title');
    if (pageTitle) {
        const titles = {
            'dashboard': 'Dashboard Overview',
            'inventory': 'Inventory Management',
            'inbound': 'Inbound Shipments',
            'outbound': 'Outbound Orders'
        };
        pageTitle.textContent = titles[sectionName] || 'Dashboard';
    }
    
    // Load section-specific data
    loadSectionData(sectionName);
}

// Load data for specific sections
async function loadSectionData(sectionName) {
    console.log('📊 Loading data for section:', sectionName);
    
    try {
        switch (sectionName) {
            case 'inventory':
                await loadInventoryData();
                break;
            case 'inbound':
                await loadInboundData();
                break;
            case 'outbound':
                await loadOutboundData();
                break;
            default:
                // Dashboard section already loads on init
                break;
        }
    } catch (error) {
        console.error('❌ Error loading section data:', error);
    }
}

// Load inventory data
async function loadInventoryData() {
    try {
        const response = await fetch(`${dashboard.apiBaseUrl}/api/inventory/summary`);
        const data = await response.json();
        
        console.log('📦 Inventory data:', data);
        
        // Update inventory table
        const inventoryTable = document.getElementById('inventory-table');
        if (inventoryTable && data.inventory) {
            const tbody = inventoryTable.querySelector('tbody');
            if (tbody) {
                tbody.innerHTML = data.inventory.map(item => `
                    <tr>
                        <td>${item.sku}</td>
                        <td>${item.name}</td>
                        <td>${item.category}</td>
                        <td>${item.location}</td>
                        <td>${item.available_quantity}</td>
                        <td>${item.reorder_level}</td>
                        <td><span class="status ${item.available_quantity > item.reorder_level ? 'in-stock' : 'low-stock'}">
                            ${item.available_quantity > item.reorder_level ? 'In Stock' : 'Low Stock'}
                        </span></td>
                    </tr>
                `).join('');
            }
        }
        
    } catch (error) {
        console.error('❌ Error loading inventory:', error);
    }
}

// Load inbound data
async function loadInboundData() {
    try {
        const response = await fetch(`${dashboard.apiBaseUrl}/api/inbound/shipments`);
        const data = await response.json();
        
        console.log('📥 Inbound data:', data);
        
        // Handle both array and object formats
        const shipments = Array.isArray(data) ? data : data.shipments || [];
        
        // Update inbound table if it exists
        const inboundTable = document.getElementById('inbound-table');
        if (inboundTable) {
            const tbody = inboundTable.querySelector('tbody');
            if (tbody) {
                if (shipments.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #666;">No inbound shipments</td></tr>';
                } else {
                    tbody.innerHTML = shipments.map(shipment => `
                        <tr>
                            <td>${shipment.shipment_id || shipment.id || 'N/A'}</td>
                            <td>${shipment.supplier || shipment.vendor || 'N/A'}</td>
                            <td>${shipment.expected_date ? new Date(shipment.expected_date).toLocaleDateString() : 'N/A'}</td>
                            <td>${shipment.arrival_date ? new Date(shipment.arrival_date).toLocaleDateString() : '-'}</td>
                            <td><span class="status status-${shipment.status || 'pending'}">${shipment.status || 'pending'}</span></td>
                            <td>${shipment.items_count || '0'}</td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="viewShipment('${shipment.id}')">View</button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
        }
        
    } catch (error) {
        console.error('❌ Error loading inbound data:', error);
    }
}

// Load outbound data
async function loadOutboundData() {
    try {
        const response = await fetch(`${dashboard.apiBaseUrl}/api/outbound/orders`);
        const data = await response.json();
        
        console.log('📤 Outbound data:', data);
        
        // Handle both array and object formats
        const orders = Array.isArray(data) ? data : data.orders || [];
        
        // Update outbound table if it exists
        const outboundTable = document.getElementById('outbound-table');
        if (outboundTable) {
            const tbody = outboundTable.querySelector('tbody');
            if (tbody) {
                if (orders.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; color: #666;">No outbound orders</td></tr>';
                } else {
                    tbody.innerHTML = orders.map(order => `
                        <tr>
                            <td>${order.order_id || order.id || 'N/A'}</td>
                            <td>${order.customer || 'N/A'}</td>
                            <td>${order.order_date ? new Date(order.order_date).toLocaleDateString() : 'N/A'}</td>
                            <td>${order.expected_dispatch ? new Date(order.expected_dispatch).toLocaleDateString() : '-'}</td>
                            <td><span class="status status-${order.status || 'pending'}">${order.status || 'pending'}</span></td>
                            <td>${order.items_count || '0'}</td>
                            <td>
                                <button class="btn btn-sm btn-primary" onclick="viewOrder('${order.id}')">View</button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
        }
        
    } catch (error) {
        console.error('❌ Error loading outbound data:', error);
    }
}

// Make functions globally available
window.showSection = showSection;
window.loadSectionData = loadSectionData;

// Placeholder functions for modals and actions
window.showAddProductModal = () => console.log('Add Product Modal - Not implemented yet');
window.showCreateShipmentModal = () => console.log('Create Shipment Modal - Not implemented yet');
window.showCreateOrderModal = () => console.log('Create Order Modal - Not implemented yet');
window.viewShipment = (id) => console.log('View Shipment:', id);
window.viewOrder = (id) => console.log('View Order:', id);
