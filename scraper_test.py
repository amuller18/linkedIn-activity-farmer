from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Define a function to handle the click event
handle_click_script = """
function handle_click(event) {
    var element = event.target;
    var element_class = element.getAttribute("class");
    window.pyweb.recordClass(element_class);
}

document.addEventListener('click', handle_click);
"""

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # You can change the webdriver according to your browser preference
driver.get("https://www.linkedin.com/home")  # Change URL to the desired website

# Inject the handle_click function into the browser's window object
driver.execute_script("window.pyweb = {};")
driver.execute_script(handle_click_script)

# Define a function to record the class of the clicked element
def record_class(class_name):
    print("Class of the clicked element:", class_name)

# Inject the record_class function into the browser's window object
driver.execute_script("window.pyweb.recordClass = arguments[0];", record_class)

# Keep the script running to allow clicking on elements
input("Click on any element. Press Enter to quit...")

# Close the browser
driver.quit()