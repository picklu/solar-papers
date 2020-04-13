
(() => {
    var pageNumber = localStorage.getItem("pageNumber") || 1;
    var paperNumber = localStorage.getItem("paperNumber") || 1;

    const postData = (data) => {
        fetch('/status',
            {
                body: data,
                method: "post"
            }).then(response => response.json())
            .then(result => console.log(result))
            .catch(error => console.log(error));
    };

    const openBrowser = (query) => {
        const url = "https://www.google.com/search?q=" + query;
        window.open(url);
    };

    const displayStatus = () => {
        document.querySelector(".status__page-info").textContent = pageNumber;
        document.querySelector(".status__row-info").textContent = paperNumber;
    };

    const updateStatusPage = event => {
        const match = window.location.href.match(/\?page=([\d]*)/)
        pageNumber = match ? parseInt(match[1]) : 1;
        paperNumber = localStorage.getItem("paperNumber") || 1;
        localStorage.setItem("pageNumber", pageNumber);
        localStorage.setItem("paperNumber", paperNumber);
        displayStatus();
    }

    const updateStatusRow = event => {
        const target = event.target;
        let formData = new FormData();
        let query;

        if (target.nodeName === "TD" && target.className === "query") {
            const rowId = target.parentElement.id;
            paperNumber = parseInt(rowId.split("-")[1]) + 1;
            query = target.textContent;
            localStorage.setItem("paperNumber", paperNumber);
            formData.append('paperNumber', paperNumber);
            formData.append('pageNumber', pageNumber);
            postData(formData);
        }
        displayStatus();

        if (!!query) {
            openBrowser(query);
        }
    };
    window.addEventListener('load', updateStatusPage);
    document.addEventListener("click", updateStatusRow);
})()