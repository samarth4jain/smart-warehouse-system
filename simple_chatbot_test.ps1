# Simple Chatbot Validation Test
Write-Host "🤖 Simple Chatbot Test" -ForegroundColor Cyan

$baseUrl = "http://localhost:8000/api/chat/message"
$queries = @("hello", "check inventory", "find wireless mouse", "show low stock", "help")

$success = 0
foreach ($query in $queries) {
    try {
        $body = @{ message = $query } | ConvertTo-Json
        $response = Invoke-RestMethod -Uri $baseUrl -Method Post -Body $body -ContentType "application/json"
        
        Write-Host "✅ '$query' -> Intent: $($response.intent)" -ForegroundColor Green
        $success++
    }
    catch {
        Write-Host "❌ '$query' -> Failed" -ForegroundColor Red
    }
}

Write-Host "`n📊 Results: $success/$($queries.Count) successful" -ForegroundColor Yellow
Write-Host "📁 Full results in: chatbot_test_results.json & chatbot_test_results.md" -ForegroundColor White
