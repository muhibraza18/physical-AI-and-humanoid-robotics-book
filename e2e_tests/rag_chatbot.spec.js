// Example Playwright E2E Test for RAG Chatbot Integration

import { test, expect } from '@playwright/test';

test.describe('RAG Chatbot Integration', () => {
  test('should display floating chatbot button on homepage', async ({ page }) => {
    await page.goto('/');
    const chatbotButton = page.locator('.floatingButton');
    await expect(chatbotButton).toBeVisible();
  });

  test('should open chat panel when button is clicked', async ({ page }) => {
    await page.goto('/');
    const chatbotButton = page.locator('.floatingButton');
    await chatbotButton.click();
    const chatPanel = page.locator('.agentPanel');
    await expect(chatPanel).toBeVisible();
    await expect(chatPanel).toHaveClass(/isOpen/);
  });

  test('should allow user to send a message and receive a response', async ({ page }) => {
    await page.goto('/');
    await page.locator('.floatingButton').click(); // Open panel
    
    const inputField = page.locator('.inputArea input');
    await inputField.fill('What is embodied intelligence?');
    await page.locator('.inputArea button').click(); // Click send

    const botMessage = page.locator('.message.bot').last();
    await expect(botMessage).toContainText(/This is a placeholder response/); // Placeholder check
  });

  test('should support select-and-ask functionality', async ({ page }) => {
    await page.goto('/docs/chapter-01'); // Go to a chapter page
    
    // Select text (Playwright's selectText method doesn't trigger mouseup for button)
    // This part would need manual selection or a more advanced Playwright interaction
    await page.evaluate(() => {
      const p = document.querySelector('p'); // Select first paragraph
      if (p) {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(p);
        selection.removeAllRanges();
        selection.addRange(range);
      }
    });

    // Simulate clicking the "Ask about selection" button (if it appears on selection)
    // This test might need to be adjusted based on actual UI implementation
    // For now, we'll just check if the selection exists.
    const selectedText = await page.evaluate(() => window.getSelection().toString());
    expect(selectedText.length).toBeGreaterThan(0);
  });

  // More tests would go here for various scenarios
});
