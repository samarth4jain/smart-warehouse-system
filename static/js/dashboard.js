// Dashboard JavaScript
class DashboardManager {
    constructor() {
        this.currentSection = 'dashboard';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDashboardData();
        this.updateWelcomeTime();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                if (link.getAttribute('onclick')) return; // Skip if has onclick
                
                e.preventDefault();
                const href = link.getAttribute('href');
                if (href && href !== '#') {
                    window.location.href = href;
                }
            });
        });

        // Auto-refresh every 30 seconds
        setInterval(() => this.refreshData(), 30000);
    }

    updateWelcomeTime() {
        const timeElement = document.getElementById('welcome-time');
        if (timeElement) {
            timeElement.textContent = new Date().toLocaleTimeString();
        }
    }

    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show selected section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        // Update page title
        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = this.getSectionTitle(sectionName);
        }

        // Update active nav item
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });

        // Load section data
        this.currentSection = sectionName;
        this.loadSectionData(sectionName);
    }

    getSectionTitle(sectionName) {
        const titles = {
            'dashboard': 'Dashboard Overview',
            'inventory': 'Inventory Management',
            'inbound': 'Inbound Shipments',
            'outbound': 'Outbound Orders'
        };
        return titles[sectionName] || 'Dashboard';
    }

    async loadDashboardData() {
        this.showLoading();
        
        try {
            const [overview, alerts, activity] = await Promise.all([
                this.apiCall('/api/dashboard/overview'),
                this.apiCall('/api/dashboard/inventory-alerts'),
                this.apiCall('/api/dashboard/recent-activity')
            ]);

            this.updateMetrics(overview);
            this.updateAlerts(alerts);
            this.updateActivity(activity);
        } catch (error) {
            this.showToast('Error loading dashboard data', 'error');
            console.error('Dashboard load error:', error);
        } finally {
            this.hideLoading();
        }
    }

    async loadSectionData(sectionName) {
        switch (sectionName) {
            case 'inventory':
                await this.loadInventoryData();
                break;
            case 'inbound':
                await this.loadInboundData();
                break;
            case 'outbound':
                await this.loadOutboundData();
                break;
        }
    }

    async loadInventoryData() {
        try {
            const data = await this.apiCall('/api/inventory/summary');
            this.updateInventoryTable(data);
            this.updateInventorySummary(data);
        } catch (error) {
            this.showToast('Error loading inventory data', 'error');
        }
    }

    async loadInboundData() {
        try {
            const data = await this.apiCall('/api/inbound/shipments');
            this.updateInboundTable(data);
        } catch (error) {
            this.showToast('Error loading inbound data', 'error');
        }
    }

    async loadOutboundData() {
        try {
            const data = await this.apiCall('/api/outbound/orders');
            this.updateOutboundTable(data);
        } catch (error) {
            this.showToast('Error loading outbound data', 'error');
        }
    }

    updateMetrics(data) {
        document.getElementById('total-products').textContent = data.inventory.total_products || 0;
        document.getElementById('low-stock-items').textContent = data.inventory.low_stock_items || 0;
        document.getElementById('pending-inbound').textContent = data.operations.pending_inbound || 0;
        document.getElementById('pending-outbound').textContent = data.operations.pending_outbound || 0;
    }

    updateAlerts(data) {
        const container = document.getElementById('alerts-container');
        if (!container) return;

        if (!data.alerts || data.alerts.length === 0) {
            container.innerHTML = '<p class="text-center text-gray-500">No active alerts</p>';
            return;
        }

        container.innerHTML = data.alerts.map(alert => `
            <div class="alert-item ${alert.severity}">
                <div class="alert-icon">
                    <i class="fas ${this.getAlertIcon(alert.type)}"></i>
                </div>
                <div class="alert-content">
                    <h4>${alert.message}</h4>
                    <p>${this.formatAlertDetails(alert.details)}</p>
                </div>
            </div>
        `).join('');
    }

    updateActivity(data) {
        const container = document.getElementById('activity-container');
        if (!container) return;

        if (!data.activities || data.activities.length === 0) {
            container.innerHTML = '<p class="text-center text-gray-500">No recent activity</p>';
            return;
        }

        container.innerHTML = data.activities.map(activity => `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="fas ${this.getActivityIcon(activity.type)}"></i>
                </div>
                <div class="activity-content">
                    <h4>${activity.description}</h4>
                    <p>${this.formatActivityDetails(activity.details)}</p>
                </div>
                <div class="activity-time">
                    ${this.formatTime(activity.timestamp)}
                </div>
            </div>
        `).join('');
    }

    updateInventoryTable(data) {
        const tbody = document.querySelector('#inventory-table tbody');
        if (!tbody) return;

        tbody.innerHTML = data.inventory.map(item => `
            <tr>
                <td>${item.sku}</td>
                <td>${item.name}</td>
                <td>${item.category || '-'}</td>
                <td>${item.available_quantity}</td>
                <td>${item.reserved_quantity}</td>
                <td>${item.quantity}</td>
                <td>${item.location || '-'}</td>
                <td>${this.getStockStatus(item)}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="dashboard.editProduct(${item.product_id})">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    updateInventorySummary(data) {
        const container = document.getElementById('inventory-summary');
        if (!container) return;

        container.innerHTML = `
            <div class="summary-stats">
                <div class="stat-item">
                    <h3>${data.total_products}</h3>
                    <p>Total Products</p>
                </div>
                <div class="stat-item warning">
                    <h3>${data.low_stock_count}</h3>
                    <p>Low Stock Items</p>
                </div>
            </div>
        `;
    }

    updateInboundTable(data) {
        const tbody = document.querySelector('#inbound-table tbody');
        if (!tbody) return;

        tbody.innerHTML = data.map(shipment => `
            <tr>
                <td>${shipment.shipment_number}</td>
                <td>${shipment.vendor?.name || '-'}</td>
                <td>${this.formatDate(shipment.expected_date)}</td>
                <td>${this.formatDate(shipment.actual_arrival_date)}</td>
                <td>${this.getStatusBadge(shipment.status)}</td>
                <td>${shipment.items?.length || 0}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="dashboard.viewShipment(${shipment.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    updateOutboundTable(data) {
        const tbody = document.querySelector('#outbound-table tbody');
        if (!tbody) return;

        tbody.innerHTML = data.map(order => `
            <tr>
                <td>${order.order_number}</td>
                <td>${order.customer?.name || '-'}</td>
                <td>${this.formatDate(order.order_date)}</td>
                <td>${this.formatDate(order.expected_dispatch_date)}</td>
                <td>${this.getStatusBadge(order.status)}</td>
                <td>${order.items?.length || 0}</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="dashboard.viewOrder(${order.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    getAlertIcon(type) {
        const icons = {
            'low_stock': 'fa-exclamation-triangle',
            'out_of_stock': 'fa-times-circle',
            'overdue': 'fa-clock'
        };
        return icons[type] || 'fa-info-circle';
    }

    getActivityIcon(type) {
        const icons = {
            'stock_movement': 'fa-exchange-alt',
            'inbound': 'fa-truck',
            'outbound': 'fa-shipping-fast'
        };
        return icons[type] || 'fa-circle';
    }

    getStockStatus(item) {
        if (item.available_quantity === 0) {
            return '<span class="status-badge danger">Out of Stock</span>';
        } else if (item.needs_reorder) {
            return '<span class="status-badge warning">Low Stock</span>';
        } else {
            return '<span class="status-badge success">In Stock</span>';
        }
    }

    getStatusBadge(status) {
        const statusClasses = {
            'pending': 'warning',
            'arrived': 'info',
            'completed': 'success',
            'dispatched': 'success',
            'delivered': 'success'
        };
        const className = statusClasses[status] || 'info';
        return `<span class="status-badge ${className}">${status}</span>`;
    }

    formatAlertDetails(details) {
        if (!details) return '';
        if (details.available !== undefined && details.reorder_level !== undefined) {
            return `Available: ${details.available}, Reorder Level: ${details.reorder_level}`;
        }
        return '';
    }

    formatActivityDetails(details) {
        if (!details) return '';
        return `${details.product || ''} (${details.sku || ''})`;
    }

    formatDate(dateString) {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleDateString();
    }

    formatTime(dateString) {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleString();
    }

    // API helper
    async apiCall(endpoint, options = {}) {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }

        return response.json();
    }

    // UI helpers
    showLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'flex';
    }

    hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.style.display = 'none';
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <p>${message}</p>
            </div>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 5000);
    }

    // Action methods
    async refreshData() {
        if (this.currentSection === 'dashboard') {
            await this.loadDashboardData();
        } else {
            await this.loadSectionData(this.currentSection);
        }
        this.showToast('Data refreshed', 'success');
    }

    editProduct(productId) {
        this.showToast('Edit product feature coming soon', 'info');
    }

    viewShipment(shipmentId) {
        this.showToast('View shipment feature coming soon', 'info');
    }

    viewOrder(orderId) {
        this.showToast('View order feature coming soon', 'info');
    }
}

// Global functions for HTML onclick handlers
function showSection(sectionName) {
    dashboard.showSection(sectionName);
}

function refreshData() {
    dashboard.refreshData();
}

function showAddProductModal() {
    dashboard.showToast('Add product feature coming soon', 'info');
}

function showCreateShipmentModal() {
    dashboard.showToast('Create shipment feature coming soon', 'info');
}

function showCreateOrderModal() {
    dashboard.showToast('Create order feature coming soon', 'info');
}

// Initialize dashboard when DOM is loaded
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new DashboardManager();
});
