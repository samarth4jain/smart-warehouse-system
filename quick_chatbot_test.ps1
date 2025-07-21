# Quick Chatbot Validation Script
# Tests essential chatbot functionality with key sample queries

Write-Host "🚀 Quick Chatbot Validation Test" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

$baseUrl = "http://localhost:8000/api/chat/message"

# Key test queries
$testQueries = @(
    @{Query = "hello"; Description = "Basic greeting test"},
    @{Query = "show low stock"; Description = "Low stock alert test"},
    @{Query = "check bluetooth headphones"; Description = "Product search test"},
    @{Query = "do we have any laptops?"; Description = "Natural language test"},
    @{Query = "show me warehouse status"; Description = "Analytics test"},
    @{Query = "help"; Description = "Help system test"}
)

$successCount = 0

foreach ($test in $testQueries) {
    try {
        Write-Host "`n🔍 Testing: $($test.Description)" -ForegroundColor Yellow
        Write-Host "Query: '$($test.Query)'" -ForegroundColor White
        
        $body = @{
            message = $test.Query
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri $baseUrl -Method POST -ContentType "application/json" -Body $body
        
        # Extract key information
        $intent = $response.intent
        $success = $response.success
        $enhanced = $response.enhanced_mode
        $confidence = $response.confidence
        
        Write-Host "✅ SUCCESS" -ForegroundColor Green
        Write-Host "   Intent: $intent" -ForegroundColor Cyan
        Write-Host "   Success: $success" -ForegroundColor Cyan
        Write-Host "   Enhanced Mode: $enhanced" -ForegroundColor Cyan
        Write-Host "   Confidence: $confidence" -ForegroundColor Cyan
        
        $successCount++
        
    } catch {
        Write-Host "❌ FAILED: $($_.Exception.Message)" -ForegroundColor Red
        
    }
}

# Summary
Write-Host "`n" + ("="*50) -ForegroundColor Gray
Write-Host "📊 VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host ("="*50) -ForegroundColor Gray

$totalCount = $testQueries.Count
$successRate = [math]::Round(($successCount / $totalCount) * 100, 1)

Write-Host "`nTotal Tests: $totalCount" -ForegroundColor White
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $($totalCount - $successCount)" -ForegroundColor Red
Write-Host "Success Rate: $successRate%" -ForegroundColor Yellow

if ($successCount -eq $totalCount) {
    Write-Host "`n🎉 ALL TESTS PASSED - CHATBOT FULLY OPERATIONAL" -ForegroundColor Green
} else {
    Write-Host "`n⚠️ SOME TESTS FAILED - CHECK CHATBOT STATUS" -ForegroundColor Yellow
}

Write-Host "`n📁 For detailed testing results, see:" -ForegroundColor White
Write-Host "   - chatbot_test_results.json (complete data)" -ForegroundColor Gray
Write-Host "   - chatbot_test_results.md (readable report)" -ForegroundColor Gray
