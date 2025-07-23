// Debug script for dashboard activity loading
console.log('🔧 Dashboard Activity Debug Script loaded');

// Wait for page to load
document.addEventListener('DOMContentLoaded', async () => {
    console.log('📋 DOM loaded, checking activity container...');
    
    const activityContainer = document.getElementById('activity-container');
    console.log('Activity container found:', !!activityContainer);
    
    if (activityContainer) {
        console.log('Activity container HTML:', activityContainer.innerHTML);
        console.log('Activity container parent:', activityContainer.parentElement?.className);
    }
    
    // Test API call manually
    try {
        console.log('🌐 Testing API call...');
        const response = await fetch('http://localhost:8001/api/dashboard/recent-activity');
        const data = await response.json();
        console.log('✅ API Response:', data);
        
        if (activityContainer && data.activities) {
            console.log('🔄 Manually updating activity container...');
            
            const activityHTML = data.activities.map(activity => {
                const time = new Date(activity.timestamp).toLocaleString();
                const typeClass = activity.details?.movement_type || activity.type;
                
                return `
                    <div class="activity-item ${typeClass}" style="padding: 10px; border: 1px solid #ddd; margin: 5px 0; border-radius: 5px;">
                        <div class="activity-icon" style="display: inline-block; width: 30px; text-align: center;">
                            📋
                        </div>
                        <div class="activity-content" style="display: inline-block; margin-left: 10px;">
                            <p class="activity-description" style="margin: 0; font-weight: bold;">${activity.description}</p>
                            <span class="activity-time" style="font-size: 12px; color: #666;">${time}</span>
                        </div>
                    </div>
                `;
            }).join('');
            
            activityContainer.innerHTML = activityHTML;
            console.log('✅ Activity container updated with', data.activities.length, 'items');
        }
        
    } catch (error) {
        console.error('❌ API Error:', error);
    }
});

// Also check if the SimpleDashboard instance exists
setTimeout(() => {
    if (window.dashboard) {
        console.log('✅ Dashboard instance found:', window.dashboard);
        console.log('🔄 Manually triggering loadData...');
        window.dashboard.loadData();
    } else {
        console.warn('⚠️ Dashboard instance not found');
    }
}, 2000);
