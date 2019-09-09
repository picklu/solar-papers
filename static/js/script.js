(() => {
    
    const displayStatus = () => {
        const status = localStorage.getItem("lastViewed");
        document.querySelector('.status-info').textContent = status || 'None';
    };
    
    const updateStatus = event => {
        if (event.target.nodeName === 'TD') {
            const rowId = event.target.parentElement.id
            const rowNum = rowId.split('-')[1] + 1;
            localStorage.setItem("lastViewed", rowId);
        }
        
        displayStatus();
    };
    
    document.addEventListener('click', updateStatus);
    displayStatus();
})()