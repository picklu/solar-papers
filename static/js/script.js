(() => {
    
    const displayStatus = () => {
        const statusRowNum = localStorage.getItem("lastViewedRow");
        const statusSolarType = localStorage.getItem("lastViewedSolar");
        document.querySelector('.status__row-info').textContent = statusRowNum || 'None';
        document.querySelector('.status__solar-info').textContent = statusSolarType || 'None';
    };
    
    const updateStatus = event => {
        let rowNum = localStorage.getItem("lastViewedRow") || NaN;
        let solarType = localStorage.getItem("lastViewedSolar") || '';
        
        if (event.target.nodeName === 'TD') {
            const rowId = event.target.parentElement.id;
            solarType = rowId.split('-')[0];
            rowNum = parseInt(rowId.split('-')[1]) + 1;
            
        } else if (event.target.className === 'cells') {
            solarType = event.target.textContent.toLowerCase();
        }
        
        localStorage.setItem("lastViewedRow", rowNum);
        localStorage.setItem("lastViewedSolar", solarType);
        displayStatus();
    };
    
    document.addEventListener('click', updateStatus);
    displayStatus();
})()