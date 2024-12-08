import asyncio
from playwright.async_api import async_playwright

"""
#1 Successfully add items to the cart and display the correct item count.
#2 Able to check out regardless of the contents in the cart.
"""

async def test_cart_operations(user_credentials: list[dict]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto('https://www.saucedemo.com/')

        for credentials in user_credentials:
            user_name = credentials['username']
            password = credentials['password']

            print(f"\nTesting for credentials Username= {user_name} and Password= {password}")

           
            await page.fill('#user-name', user_name)
            await page.fill('#password', password)
            await page.click('#login-button')

            try:
                await page.wait_for_selector(".inventory_list", timeout=3000)
                print(f"Successfully logged in as {user_name}!")

                
                items = await page.query_selector_all(".inventory_item button")
                for index, item in enumerate(items):
                    await item.click()
                    cart_count = await page.inner_text(".shopping_cart_badge")
                    print(f"Added item {index + 1} to the cart. Items in cart: {cart_count}")

                
                await page.click(".shopping_cart_link")
                await page.wait_for_selector(".cart_list")
                print("Cart page opened successfully.")

                
                await page.click("#checkout")
                try:
                    await page.wait_for_selector("#checkout_info_container", timeout=3000)
                    print("Proceeded to checkout successfully.")
                except:
                    print("Checkout failed!")
                
            except Exception as e:
                print(f"Login failed or user is locked out: {e}")

            # Return to the login page for the next test
            await page.goto('https://www.saucedemo.com/')
        await browser.close()

# Test users
test_users = [
    {
        "username": "standard_user", "password": "secret_sauce",
    },
    {
        "username": "standard_user", "password": "123",
    },
    {
        "username": "locked_out_user", "password": "secret_sauce",
    }
]

asyncio.run(test_cart_operations(test_users))
