function showTab(tabId) {
    // Get all tabs
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-button');

    // Hide all tabs
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    buttons.forEach(button => {
        button.classList.remove('active');
    });

    // Show the selected tab
    document.getElementById(tabId).classList.add('active');

    // Add active class to the clicked button
    const activeButton = document.querySelector(`button[onclick="showTab('${tabId}')"]`);
    activeButton.classList.add('active');
}
