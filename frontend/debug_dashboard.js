// Simple dashboard debug script
console.log('🚀 Dashboard debug script loaded');

const API_BASE_URL = 'http://localhost:8001';

async function debugDashboard() {
    console.log('🔍 Starting dashboard debug...');
    
    try {
        // Test API call
        console.log('📡 Making API call to:', `${API_BASE_URL}/api/dashboard/overview`);
        const response = await fetch(`${API_BASE_URL}/api/dashboard/overview`);
        console.log('📥 Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('📊 API Data received:', data);
        
        // Check DOM elements
        const elements = {
            totalProducts: document.getElementById('total-products'),
            lowStock: document.getElementById('low-stock-items'),
            pendingInbound: document.getElementById('pending-inbound'),
            pendingOutbound: document.getElementById('pending-outbound')
        };
        
        console.log('🎯 DOM Elements check:', {
            totalProducts: !!elements.totalProducts,
            lowStock: !!elements.lowStock,
            pendingInbound: !!elements.pendingInbound,
            pendingOutbound: !!elements.pendingOutbound
        });
        
        // Update elements manually
        if (elements.totalProducts) {
            elements.totalProducts.textContent = data.inventory.total_products;
            console.log('✅ Updated total-products to:', data.inventory.total_products);
        }
        
        if (elements.lowStock) {
            elements.lowStock.textContent = data.inventory.low_stock_items;
            console.log('✅ Updated low-stock-items to:', data.inventory.low_stock_items);
        }
        
        if (elements.pendingInbound) {
            elements.pendingInbound.textContent = data.operations.pending_inbound;
            console.log('✅ Updated pending-inbound to:', data.operations.pending_inbound);
        }
        
        if (elements.pendingOutbound) {
            elements.pendingOutbound.textContent = data.operations.pending_outbound;
            console.log('✅ Updated pending-outbound to:', data.operations.pending_outbound);
        }
        
        console.log('🎉 Dashboard debug completed successfully!');
        
    } catch (error) {
        console.error('❌ Dashboard debug failed:', error);
    }
}

// Run debug when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', debugDashboard);
} else {
    debugDashboard();
}

// Also add to global scope for manual testing
window.debugDashboard = debugDashboard;
