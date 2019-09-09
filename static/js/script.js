(() => {
    
    const openBrowser = (query) => {
        const url = "https://www.google.com/search?q=" + query;
        window.open(url);
    }
    
    const displayStatus = () => {
        const statusSolarType = localStorage.getItem("lastViewedSolar") || "None";
        let statusRowNum = undefined;
        
        if (statusSolarType === 'dsscs') {
            statusRowNum = localStorage.getItem("lastViewedDSSCs");
        } else if (statusSolarType === 'prscs') {
            statusRowNum = localStorage.getItem("lastViewedPrSCs");
        }
       
        document.querySelector(".status__solar-info").textContent = statusSolarType;
        document.querySelector(".status__row-info").textContent = statusRowNum || "None";

    };
    
    const updateStatus = event => {
        const target = event.target;
        let solarType = localStorage.getItem("lastViewedSolar") || "";
        let query = "";
        
        if (target.nodeName === "TD" && target.className === "query") {
            const rowId = target.parentElement.id;
            const rowNum = parseInt(rowId.split("-")[1]) + 1;
            query = target.textContent;
            solarType = rowId.split("-")[0];
            
             if (solarType === 'dsscs') {
                localStorage.setItem("lastViewedDSSCs", rowNum);
            } else if (solarType === 'prscs') {
                localStorage.setItem("lastViewedPrSCs", rowNum);
            }
           
        } else if (target.className === "cells") {
            solarType = event.target.textContent.toLowerCase();
        }

        localStorage.setItem("lastViewedSolar", solarType);
        
        displayStatus();
        
        if (!!query) {
            openBrowser(query);
        }
    };
    
    document.addEventListener("click", updateStatus);
    displayStatus();
})()