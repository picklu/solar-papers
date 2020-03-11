(() => {
    var pageNumber = localStorage.getItem("pageNumber") || 1;
    var rowNumber = localStorage.getItem("rowNumber") || 1;

    const openBrowser = (query) => {
        const url = "https://www.google.com/search?q=" + query;
        window.open(url);
    }

    const displayStatus = () => {
        document.querySelector(".status__page-info").textContent = pageNumber;
        document.querySelector(".status__row-info").textContent = rowNumber;
    };

    const updateStatus = event => {
        const target = event.target;
        let query;

        if (target.nodeName === "TD" && target.className === "query") {
            const rowId = target.parentElement.id;
            pageNumber = parseInt(window.location.href.split("=")[1]) || 1;
            rowNumber = parseInt(rowId.split("-")[1]) + 1;
            query = target.textContent;

            localStorage.setItem("pageNumber", pageNumber);
            localStorage.setItem("rowNumber", rowNumber);

        }
        displayStatus();

        if (!!query) {
            openBrowser(query);
        }
    };

    document.addEventListener("click", updateStatus);
    displayStatus();
})()