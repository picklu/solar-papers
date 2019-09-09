(() => {
    
    const openBrowser = (query) => {
        const url = "https://www.google.com/search?q=" + query;
        window.open(url);
    }
    
    const displayStatus = () => {
        const statusRowNum = localStorage.getItem("lastViewedRow");
        const statusSolarType = localStorage.getItem("lastViewedSolar");
        document.querySelector('.status__row-info').textContent = statusRowNum || "None";
        document.querySelector('.status__solar-info').textContent = statusSolarType || "None";
    };
    
    const updateStatus = event => {
        const target = event.target;
        let rowNum = localStorage.getItem("lastViewedRow") || NaN;
        let solarType = localStorage.getItem("lastViewedSolar") || '';
        let query = "";
        
        if (target.nodeName === "TD" && target.className === "query") {
            const rowId = target.parentElement.id;
            solarType = rowId.split("-")[0];
            rowNum = parseInt(rowId.split("-")[1]) + 1;
            query = target.textContent;
        } else if (target.className === "cells") {
            solarType = event.target.textContent.toLowerCase();
        }

        localStorage.setItem("lastViewedRow", rowNum);
        localStorage.setItem("lastViewedSolar", solarType);
        displayStatus();
        
        if (!!query) {
            openBrowser(query);
        }
    };
    
    document.addEventListener("click", updateStatus);
    displayStatus();
})()