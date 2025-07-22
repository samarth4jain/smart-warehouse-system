# Comprehensive Chatbot Testing Results

**Test Date:** 2025-07-20 14:25:36
**Session ID:** test_session_1753001476
**Base URL:** http://localhost:8000
**Total Queries Tested:** 118

## 📊 Overall Statistics

- **Total Queries:** 118
- **Successful:** 118 (100.0%)
- **Failed:** 0 (0.0%)
- **Average Response Time:** 2099.64 ms

## 📂 Category Statistics

### Basic Greetings & Conversation
- **Total:** 13
- **Successful:** 13 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2100.75 ms

### Inventory Management Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2103.26 ms

### Product Search Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2100.41 ms

### Natural Language Alert Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2113.75 ms

### Casual & Conversational Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2093.04 ms

### SKU & Code-based Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2105.97 ms

### Analytics & Reporting Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2098.25 ms

### Operations & Status Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2094.71 ms

### Help & Support Queries
- **Total:** 13
- **Successful:** 13 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2097.3 ms

### Edge Cases & Error Handling
- **Total:** 12
- **Successful:** 12 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2090.27 ms

### Complex & Multi-intent Queries
- **Total:** 10
- **Successful:** 10 (100.0%)
- **Failed:** 0
- **Avg Response Time:** 2100.56 ms

## 📝 Detailed Test Results

### Basic Greetings & Conversation

✅ **Query:** `hello`
**Description:** Basic greeting
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2119.25 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `hi there`
**Description:** Casual greeting
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2073.79 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `good morning`
**Description:** Time-specific greeting
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2072.8 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `hey`
**Description:** Very casual greeting
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2089.38 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `hi`
**Description:** Simple greeting
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2116.41 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `good afternoon`
**Description:** Afternoon greeting
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2108.17 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what's up?`
**Description:** Slang greeting
**Intent:** general_query
**Confidence:** 0.3
**Response Time:** 2107.71 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'm here to help with your warehouse operations! 🏭  I can check stock, process orders, handle deliveries, and much more.  Try asking me something like: • 'Do we have any laptops?' • 'Process the deliv...
**Suggestions:** Ask about stock levels, Check order status, Process a delivery

---

✅ **Query:** `how are you?`
**Description:** Personal inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2088.03 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `thanks`
**Description:** Gratitude expression
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2117.85 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `thank you`
**Description:** Formal thanks
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2103.83 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `bye`
**Description:** Farewell
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2108.15 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `goodbye`
**Description:** Formal farewell
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2134.19 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `see you later`
**Description:** Casual farewell
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2070.22 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Inventory Management Queries

✅ **Query:** `show low stock`
**Description:** Direct low stock query
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2125.28 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: alerts_monitoring)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `check inventory`
**Description:** General inventory check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2074.52 ms
**Enhanced Mode:** True
**Success Status:** False
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** **PRODUCT SEARCH RESULT**: No matches found  Search term: 'Inventory' Recommendations: • Verify product name or SKU code • Use exact product naming • Check product database integrity
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `what's in stock?`
**Description:** Casual stock inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2110.52 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me all products`
**Description:** Product listing request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2076.85 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `check stock levels`
**Description:** Stock level inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2096.97 ms
**Enhanced Mode:** True
**Success Status:** False
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Hmm, I couldn't find anything for 'Stock Levels' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `what products do we have?`
**Description:** Product catalog request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2115.86 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show inventory summary`
**Description:** Inventory overview
**Intent:** inventory_check
**Confidence:** 0.9
**Response Time:** 2094.07 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** **INVENTORY QUERY** - Additional information required  Please provide: • Product name or SKU code • Specific product identifier  Format examples: • 'Check stock SKU: PROD001' • 'Inventory status for P...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `check warehouse inventory`
**Description:** Warehouse inventory check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2124.17 ms
**Enhanced Mode:** True
**Success Status:** False
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** **PRODUCT SEARCH RESULT**: No matches found  Search term: 'Warehouse' Recommendations: • Verify product name or SKU code • Use exact product naming • Check product database integrity
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `what items are available?`
**Description:** Availability inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2090.91 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `display current stock`
**Description:** Stock display request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2123.43 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Product Search Queries

✅ **Query:** `check bluetooth headphones`
**Description:** Specific product search
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2079.29 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Heads up! We're running low on **Bluetooth Headphones** 🔔  📦 Available: 8 Each 🔒 Reserved: 0 Each 📍 Location: A1-03 ⚠️ Reorder level: 15 Each  💡 **Suggestion**: Might want to reorder soon!
**Data Available:** Yes
**Suggestions:** Reorder this product soon, Check usage patterns, Adjust reorder levels

---

✅ **Query:** `find wireless mouse`
**Description:** Product search with 'find'
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2096.77 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `look for laptop`
**Description:** Product search with 'look for'
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2113.38 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `search for keyboard`
**Description:** Product search with 'search'
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2077.75 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `do we have monitors?`
**Description:** Casual product inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2112.57 ms
**Enhanced Mode:** True
**Success Status:** False
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Hmm, I couldn't find anything for 'Monitors?' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `check office chair`
**Description:** Office furniture search
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2118.18 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Heads up! We're running low on **Office Chair** 🔔  📦 Available: 3 Each 🔒 Reserved: 0 Each 📍 Location: B1-01 ⚠️ Reorder level: 5 Each  💡 **Suggestion**: Might want to reorder soon!
**Data Available:** Yes
**Suggestions:** Reorder this product soon, Check usage patterns, Adjust reorder levels

---

✅ **Query:** `where is the laptop?`
**Description:** Product location inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2096.94 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Laptop** ✅  📦 Available: 25 Each 🔒 Reserved: 0 Each 📍 Location: A1-01  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `show me wireless mouse details`
**Description:** Detailed product info
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2095.28 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what about bluetooth devices?`
**Description:** Category search
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2113.8 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `check electronic items`
**Description:** Category-based search
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2100.13 ms
**Enhanced Mode:** True
**Success Status:** False
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Hmm, I couldn't find anything for 'Electronic Items' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

### Natural Language Alert Queries

✅ **Query:** `what items are running low?`
**Description:** Natural language low stock
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2120.6 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: alerts_monitoring)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `what needs attention?`
**Description:** General attention query
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2092.52 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: alerts_monitoring)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `any items need reordering?`
**Description:** Reorder inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2090.78 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: alerts_monitoring)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me problem areas`
**Description:** Problem identification
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2078.51 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: alerts_monitoring)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what's critically low?`
**Description:** Critical stock inquiry
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2130.46 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: alerts_monitoring)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `are we running out of anything?`
**Description:** Stock depletion check
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2116.11 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: alerts_monitoring)
**Response:** Hey there! Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 item...
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `what should I be worried about?`
**Description:** Concern-based query
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2126.49 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: alerts_monitoring)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `which products need attention?`
**Description:** Product attention query
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2063.16 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: alerts_monitoring)
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `any red flags in inventory?`
**Description:** Alert metaphor query
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2108.84 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: alerts_monitoring)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `what items are in trouble?`
**Description:** Trouble identification
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2210.01 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: alerts_monitoring)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Casual & Conversational Queries

✅ **Query:** `do we have any laptops?`
**Description:** Casual availability check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2067.9 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Laptop** ✅  📦 Available: 25 Each 🔒 Reserved: 0 Each 📍 Location: A1-01  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `got any wireless mice?`
**Description:** Slang availability check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2131.65 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Wireless Mouse** ✅  📦 Available: 45 Each 🔒 Reserved: 0 Each 📍 Location: A1-02  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `how many keyboards are there?`
**Description:** Quantity inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2102.83 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `are there enough office chairs?`
**Description:** Sufficiency inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2093.85 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `do we still have bluetooth headphones?`
**Description:** Continuing availability
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2085.57 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `is there any laptop left?`
**Description:** Remaining stock inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2074.36 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `how much stuff do we have?`
**Description:** General quantity inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2100.0 ms
**Enhanced Mode:** True
**Success Status:** False
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Hmm, I couldn't find anything for 'Stuff' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `what's the deal with monitors?`
**Description:** Casual status inquiry
**Intent:** general_query
**Confidence:** 0.3
**Response Time:** 2080.85 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: inventory_check)
**Response:** I'm here to help with your warehouse operations! 🏭  I can check stock, process orders, handle deliveries, and much more.  Try asking me something like: • 'Do we have any laptops?' • 'Process the deliv...
**Suggestions:** Ask about stock levels, Check order status, Process a delivery

---

✅ **Query:** `tell me about our mouse inventory`
**Description:** Narrative inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2093.53 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** **INVENTORY QUERY** - Additional information required  Please provide: • Product name or SKU code • Specific product identifier  Format examples: • 'Check stock SKU: PROD001' • 'Inventory status for P...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `give me the lowdown on headphones`
**Description:** Informal information request
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2099.9 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: inventory_check)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

### SKU & Code-based Queries

✅ **Query:** `check SKU LAPTOP001`
**Description:** Direct SKU query
**Intent:** inventory_check
**Confidence:** 0.9
**Response Time:** 2095.63 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** **INVENTORY REPORT - STOCK ADEQUATE**  Product: Laptop SKU: LAPTOP001 Available Quantity: 25 Each Reserved Quantity: 0 Each Total Inventory: 25 Each Location: A1-01 Reorder Level: 10 Each  Status: STO...
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `show me MOUSE001`
**Description:** SKU display request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2107.91 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Wireless Mouse** ✅  📦 Available: 45 Each 🔒 Reserved: 0 Each 📍 Location: A1-02  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `what's the status of HEAD001?`
**Description:** SKU status inquiry
**Intent:** reporting_analytics
**Confidence:** 0.8
**Response Time:** 2124.12 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: inventory_check)
**Response:** Here's how things are looking in our warehouse!  📦 **Inventory Overview:** • Total Products: 5 • Total Value: $29,598.44 • Low Stock Items: 2  🚛 **Operations:** • Pending Inbound: 0 shipments • Pendin...
**Data Available:** Yes
**Suggestions:** Check low stock, View detailed reports, Check operations

---

✅ **Query:** `look up product CHAIR001`
**Description:** SKU lookup
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2100.63 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Heads up! We're running low on **Office Chair** 🔔  📦 Available: 3 Each 🔒 Reserved: 0 Each 📍 Location: B1-01 ⚠️ Reorder level: 5 Each  💡 **Suggestion**: Might want to reorder soon!
**Data Available:** Yes
**Suggestions:** Reorder this product soon, Check usage patterns, Adjust reorder levels

---

✅ **Query:** `check stock for LAPTOP001`
**Description:** SKU stock check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2110.16 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Laptop** ✅  📦 Available: 25 Each 🔒 Reserved: 0 Each 📍 Location: A1-01  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `show details for MOUSE001`
**Description:** SKU details request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2121.2 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Wireless Mouse** ✅  📦 Available: 45 Each 🔒 Reserved: 0 Each 📍 Location: A1-02  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `find product with code HEAD001`
**Description:** Code-based search
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2079.0 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Heads up! We're running low on **Bluetooth Headphones** 🔔  📦 Available: 8 Each 🔒 Reserved: 0 Each 📍 Location: A1-03 ⚠️ Reorder level: 15 Each  💡 **Suggestion**: Might want to reorder soon!
**Data Available:** Yes
**Suggestions:** Reorder this product soon, Check usage patterns, Adjust reorder levels

---

✅ **Query:** `check item CHAIR001`
**Description:** Item code check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2112.84 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Heads up! We're running low on **Office Chair** 🔔  📦 Available: 3 Each 🔒 Reserved: 0 Each 📍 Location: B1-01 ⚠️ Reorder level: 5 Each  💡 **Suggestion**: Might want to reorder soon!
**Data Available:** Yes
**Suggestions:** Reorder this product soon, Check usage patterns, Adjust reorder levels

---

✅ **Query:** `what about SKU LAPTOP001?`
**Description:** Casual SKU inquiry
**Intent:** inventory_check
**Confidence:** 0.9
**Response Time:** 2100.42 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** **INVENTORY REPORT - STOCK ADEQUATE**  Product: Laptop SKU: LAPTOP001 Available Quantity: 25 Each Reserved Quantity: 0 Each Total Inventory: 25 Each Location: A1-01 Reorder Level: 10 Each  Status: STO...
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

✅ **Query:** `tell me about product MOUSE001`
**Description:** Narrative SKU request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2107.74 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: inventory_check)
**Response:** Good news! We've got plenty of **Wireless Mouse** ✅  📦 Available: 45 Each 🔒 Reserved: 0 Each 📍 Location: A1-02  💡 **Status**: Stock levels look healthy!
**Data Available:** Yes
**Suggestions:** Update stock count if needed, Check product location, Review product details

---

### Analytics & Reporting Queries

✅ **Query:** `show me warehouse status`
**Description:** Warehouse overview
**Intent:** reporting_analytics
**Confidence:** 0.9
**Response Time:** 2121.34 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: reporting_analytics)
**Response:** Here's how things are looking in our warehouse!  📦 **Inventory Overview:** • Total Products: 5 • Total Value: $29,598.44 • Low Stock Items: 2  🚛 **Operations:** • Pending Inbound: 0 shipments • Pendin...
**Data Available:** Yes
**Suggestions:** Check low stock, View detailed reports, Check operations

---

✅ **Query:** `generate inventory report`
**Description:** Report generation
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2111.54 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** **INVENTORY QUERY** - Additional information required  Please provide: • Product name or SKU code • Specific product identifier  Format examples: • 'Check stock SKU: PROD001' • 'Inventory status for P...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what's our warehouse performance?`
**Description:** Performance inquiry
**Intent:** general_query
**Confidence:** 0.3
**Response Time:** 2106.28 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'm here to help with your warehouse operations! 🏭  I can check stock, process orders, handle deliveries, and much more.  Try asking me something like: • 'Do we have any laptops?' • 'Process the deliv...
**Suggestions:** Ask about stock levels, Check order status, Process a delivery

---

✅ **Query:** `show me the analytics`
**Description:** Analytics request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2090.62 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `give me a summary`
**Description:** Summary request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2115.75 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `how are we doing today?`
**Description:** Performance check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2104.29 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show dashboard`
**Description:** Dashboard request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2106.99 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what are the metrics?`
**Description:** Metrics inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2090.6 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `display warehouse overview`
**Description:** Overview request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2074.59 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me key statistics`
**Description:** Statistics request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2060.49 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Operations & Status Queries

✅ **Query:** `how are operations today?`
**Description:** Daily operations check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2099.97 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what's happening in the warehouse?`
**Description:** Activity inquiry
**Intent:** reporting_analytics
**Confidence:** 0.8
**Response Time:** 2093.99 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: reporting_analytics)
**Response:** Here's how things are looking in our warehouse!  📦 **Inventory Overview:** • Total Products: 5 • Total Value: $29,598.44 • Low Stock Items: 2  🚛 **Operations:** • Pending Inbound: 0 shipments • Pendin...
**Data Available:** Yes
**Suggestions:** Check low stock, View detailed reports, Check operations

---

✅ **Query:** `show me today's activities`
**Description:** Daily activity request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2073.27 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `any deliveries today?`
**Description:** Delivery inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2081.08 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: operations_check)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what's the warehouse status?`
**Description:** Status inquiry
**Intent:** reporting_analytics
**Confidence:** 0.9
**Response Time:** 2073.5 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ✅ (Expected: reporting_analytics)
**Response:** Here's how things are looking in our warehouse!  📦 **Inventory Overview:** • Total Products: 5 • Total Value: $29,598.44 • Low Stock Items: 2  🚛 **Operations:** • Pending Inbound: 0 shipments • Pendin...
**Data Available:** Yes
**Suggestions:** Check low stock, View detailed reports, Check operations

---

✅ **Query:** `how is everything running?`
**Description:** General operations check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2107.64 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me current operations`
**Description:** Operations overview
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2107.27 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what's going on today?`
**Description:** Activity summary
**Intent:** general_query
**Confidence:** 0.3
**Response Time:** 2103.79 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'm here to help with your warehouse operations! 🏭  I can check stock, process orders, handle deliveries, and much more.  Try asking me something like: • 'Do we have any laptops?' • 'Process the deliv...
**Suggestions:** Ask about stock levels, Check order status, Process a delivery

---

✅ **Query:** `any issues with operations?`
**Description:** Issue identification
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2097.79 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `how smooth are operations?`
**Description:** Operations quality check
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2108.8 ms
**Enhanced Mode:** True
**Success Status:** True
**Intent Match:** ❌ (Expected: reporting_analytics)
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Help & Support Queries

✅ **Query:** `help`
**Description:** Basic help request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2112.12 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what can you do?`
**Description:** Capability inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2103.04 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd be happy to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much i...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `how do I use this?`
**Description:** Usage inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2104.32 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what features are available?`
**Description:** Feature inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2085.31 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `can you help me?`
**Description:** Help request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2095.64 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd be happy to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much i...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what commands work?`
**Description:** Command inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2124.18 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me examples`
**Description:** Example request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2087.96 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `how does this work?`
**Description:** Functionality inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2097.9 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what are your capabilities?`
**Description:** Capability question
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2089.14 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `guide me`
**Description:** Guidance request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2082.87 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `I need assistance`
**Description:** Assistance request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2107.0 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `what can I ask you?`
**Description:** Query scope inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2095.82 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me what you can do`
**Description:** Demonstration request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2079.64 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Edge Cases & Error Handling

✅ **Query:** ``
**Description:** Empty query
**Intent:** empty_input
**Confidence:** 1.0
**Response Time:** 2061.93 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** I didn't receive a message. Please try asking me something about your warehouse operations.
**Suggestions:** Check inventory, View alerts, Get help

---

✅ **Query:** `check nonexistent product`
**Description:** Non-existent product
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2099.47 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** Hmm, I couldn't find anything for 'Nonexistent Product' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `find product XYZ123`
**Description:** Invalid product code
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2105.59 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** Hmm, I couldn't find anything for 'XYZ123' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `show me unicorns`
**Description:** Nonsense product
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2120.24 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `asdfghjkl`
**Description:** Random characters
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2100.95 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `check product with very long name that doesn't exist`
**Description:** Long non-existent product
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2075.37 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** Hmm, I couldn't find anything for 'Product With Very Long Name That Doesn'T Exist' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me t...
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `find something`
**Description:** Vague request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2085.31 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `show me everything about nothing`
**Description:** Contradictory request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2080.56 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `check inventory for mars rovers`
**Description:** Impossible product
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2065.17 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** **PRODUCT SEARCH RESULT**: No matches found  Search term: 'Inventory For Mars Rovers' Recommendations: • Verify product name or SKU code • Use exact product naming • Check product database integrity
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `123456789`
**Description:** Numbers only
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2090.07 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `!@#$%^&*()`
**Description:** Special characters only
**Intent:** general_query
**Confidence:** 0.3
**Response Time:** 2097.52 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'm here to help with your warehouse operations! 🏭  I can check stock, process orders, handle deliveries, and much more.  Try asking me something like: • 'Do we have any laptops?' • 'Process the deliv...
**Suggestions:** Ask about stock levels, Check order status, Process a delivery

---

✅ **Query:** `find . . . .`
**Description:** Dots only
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2101.09 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

### Complex & Multi-intent Queries

✅ **Query:** `show me low stock items and generate a report`
**Description:** Multi-intent query
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2136.17 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `check bluetooth headphones and tell me if we need more`
**Description:** Complex inquiry
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2103.16 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Heads up! We're running low on **Bluetooth Headphones** 🔔  📦 Available: 8 Each 🔒 Reserved: 0 Each 📍 Location: A1-03 ⚠️ Reorder level: 15 Each  💡 **Suggestion**: Might want to reorder soon!
**Data Available:** Yes
**Suggestions:** Reorder this product soon, Check usage patterns, Adjust reorder levels

---

✅ **Query:** `what items are low and how can I fix it?`
**Description:** Problem + solution query
**Intent:** alerts_monitoring
**Confidence:** 0.8
**Response Time:** 2109.38 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Here's what needs attention in our warehouse! 🔔  ⚠️ **LOW STOCK:** • **Bluetooth Headphones** - 8 Each left • **Office Chair** - 3 Each left  💡 **Action needed**: Consider reordering 2 items
**Data Available:** Yes
**Suggestions:** Reorder critical items, View specific product, Update stock levels

---

✅ **Query:** `show warehouse status and highlight problems`
**Description:** Status + analysis
**Intent:** reporting_analytics
**Confidence:** 0.9
**Response Time:** 2114.93 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hey there! Here's how things are looking in our warehouse!  📦 **Inventory Overview:** • Total Products: 5 • Total Value: $29,598.44 • Low Stock Items: 2  🚛 **Operations:** • Pending Inbound: 0 shipmen...
**Data Available:** Yes
**Suggestions:** Check low stock, View detailed reports, Check operations

---

✅ **Query:** `find all electronics and check their stock levels`
**Description:** Category + analysis
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2094.02 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** Hmm, I couldn't find anything for 'Their' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show all products'
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `tell me about inventory and suggest improvements`
**Description:** Info + recommendation
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2083.93 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** **INVENTORY QUERY** - Additional information required  Please provide: • Product name or SKU code • Specific product identifier  Format examples: • 'Check stock SKU: PROD001' • 'Inventory status for P...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `check all products that need attention today`
**Description:** Time-bound complex query
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2062.1 ms
**Enhanced Mode:** True
**Success Status:** False
**Response:** Hmm, I couldn't find anything for 'All Products That Need Attention Today' 🤔  💡 **Try these instead:** • Use the exact product name • Try a SKU code (like PROD001) • Check for typos • Ask me to 'show ...
**Suggestions:** Try different search terms, View all products, Check product catalog

---

✅ **Query:** `show me everything that's wrong with our inventory`
**Description:** Comprehensive problem query
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2111.19 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** Hello. **INVENTORY QUERY** - Additional information required  Please provide: • Product name or SKU code • Specific product identifier  Format examples: • 'Check stock SKU: PROD001' • 'Inventory statu...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `analyze our stock and tell me what to do`
**Description:** Analysis + action request
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2070.76 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

✅ **Query:** `give me a complete picture of warehouse operations`
**Description:** Comprehensive overview
**Intent:** inventory_check
**Confidence:** 0.8
**Response Time:** 2119.97 ms
**Enhanced Mode:** True
**Success Status:** True
**Response:** I'd love to help you check stock! 😊  Could you tell me which product you're asking about?  💡 **You can say things like:** • 'Check stock for blue widgets' • 'Do we have any PROD001?' • 'How much inven...
**Suggestions:** Specify product name, Use SKU code, Browse product catalog

---

