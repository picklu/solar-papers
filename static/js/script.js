
(() => {
    var pageNumberDOM = document.getElementById('page-number');
    var paperNumberDOM = document.getElementById('paper-number');
    var pageNumber = pageNumberDOM.innerText;
    var paperNumber = paperNumberDOM.innerText;

    const openBrowser = (query) => {
        const url = "https://www.google.com/search?q=" + query;
        window.open(url);
    };

    const displayStatus = () => {
        pageNumberDOM.textContent = pageNumber;
        paperNumberDOM.textContent = paperNumber;
    };

    const postData = (data) => {
        fetch('/status',
            {
                body: data,
                method: "post"
            }).then(response => response.json())
            .then(result => console.log(result))
            .catch(error => console.log(error));
    };

    const lastVisitedPage = (event) => {
        const btnVisited = document.getElementById("btn-visited");
        if (btnVisited.id === event.target.id) {
            event.preventDefault();
            fetch('/status')
                .then(res => res.json())
                .then(data => {
                    window.location.href = `/?page=${data.pageNumber || 1}`;
                })
                .catch(error => console.log(error));
        }
    };


    const updateStatus = event => {
        const target = event.target;
        let query;

        if (target.nodeName === "TD" && target.className === "query") {
            const match = window.location.href.match(/\?page=([\d]*)/)
            const rowId = target.parentElement.id;
            const now = (new Date()).toISOString();
            let formData = new FormData();

            query = target.textContent;
            pageNumber = match ? parseInt(match[1]) : 1;
            paperNumber = parseInt(rowId.split("-")[1]) + 1;

            formData.append('paperNumber', paperNumber);
            formData.append('pageNumber', pageNumber);
            formData.append('timeStamp', now);
            postData(formData);
        }
        displayStatus();

        if (!!query) {
            openBrowser(query);
        }
    };
    document.addEventListener('click', updateStatus);
    document.addEventListener('click', lastVisitedPage);
})()