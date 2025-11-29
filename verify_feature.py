
import asyncio
from playwright.async_api import async_playwright
import time

async def verify_feature():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Open the file
        await page.goto(f"file://{os.getcwd()}/index.html")

        # Click "ENTER DASHBOARD"
        await page.click('#start-btn')
        await page.wait_for_timeout(1000)

        # Verify initial state (Normal Mode)
        classes_initial = await page.evaluate("document.body.className")
        print(f"Initial classes: '{classes_initial}'")
        if "hacker-mode" in classes_initial:
            print("FAILED: Hacker mode shouldn't be active initially.")
            await browser.close()
            return

        # Trigger Hacker Mode (5 clicks on .project-name)
        project_name = page.locator('.project-name')
        if await project_name.count() == 0:
             print("FAILED: Project Name element not found.")
             await browser.close()
             return

        for _ in range(5):
            await project_name.click()
            time.sleep(0.1)

        # Handle alert
        # Playwright auto-dismisses dialogs but we can check if class changed
        await page.wait_for_timeout(1000)

        classes_after = await page.evaluate("document.body.className")
        print(f"Classes after trigger: '{classes_after}'")

        if "hacker-mode" not in classes_after:
            print("FAILED: Hacker mode not activated after 5 clicks.")
            # Debug: maybe take screenshot
            await page.screenshot(path="debug_failed_trigger.png")
        else:
            print("SUCCESS: Hacker mode activated.")
            await page.screenshot(path="hacker_mode_proof.png")

        # Verify Persistence
        await page.reload()
        await page.click('#start-btn') # Need to enter dashboard again
        await page.wait_for_timeout(500)

        classes_reloaded = await page.evaluate("document.body.className")
        if "hacker-mode" in classes_reloaded:
            print("SUCCESS: Hacker mode persisted after reload.")
        else:
            print("FAILED: Hacker mode did not persist.")

        await browser.close()

import os
if __name__ == "__main__":
    asyncio.run(verify_feature())
