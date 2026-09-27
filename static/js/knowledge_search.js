document.addEventListener("DOMContentLoaded", () => {

    const input =
        document.getElementById("searchInput");

    const method =
        document.getElementById("searchMethod");

    const button =
        document.getElementById("searchButton");

    const resultsContainer =
        document.getElementById("searchResults");

    const status =
        document.getElementById("searchStatus");

    const methodButtons =
        document.querySelectorAll(".retrieval-method");

    const quickSearchButtons =
        document.querySelectorAll(".quick-search");


    /* =====================================================
       ICONS
    ===================================================== */

    function refreshIcons() {

        if (window.lucide) {

            lucide.createIcons();

        }

    }


    /* =====================================================
       METHOD DESCRIPTION
    ===================================================== */

    function getMethodLabel(value) {

        switch (value) {

            case "bm25":

                return "BM25";


            case "tfidf":

                return "TF-IDF";


            case "language_model":

                return "Language Model";


            default:

                return value;

        }

    }


    /* =====================================================
       UPDATE METHOD UI
    ===================================================== */

    function updateMethodUI() {

        methodButtons.forEach(button => {

            button.classList.toggle(
                "active",
                button.dataset.method ===
                method.value
            );

        });

    }


    method.addEventListener(
        "change",
        updateMethodUI
    );


    methodButtons.forEach(button => {

        button.addEventListener(
            "click",
            () => {

                method.value =
                    button.dataset.method;

                updateMethodUI();

                input.focus();

            }
        );

    });


    /* =====================================================
       SEARCH
    ===================================================== */

    async function performSearch(
        query = null
    ) {

        if (query === null) {

            query =
                input.value.trim();

        } else {

            input.value =
                query;

        }


        if (!query) {

            status.textContent =
                "Enter an HR-related query to begin.";

            input.focus();

            return;

        }


        button.disabled = true;

        button.classList.add(
            "is-loading"
        );


        button.innerHTML = `
            <span class="button-spinner"></span>
            Searching...
        `;


        status.textContent =
            `Searching with ${getMethodLabel(
                method.value
            )}...`;


        resultsContainer.innerHTML = `

            <article class="knowledge-loading-card">

                <div class="loading-ring"></div>

                <h3>
                    Retrieving documents
                </h3>

                <p>
                    Ranking HR knowledge using
                    ${escapeHtml(
                        getMethodLabel(
                            method.value
                        )
                    )}.
                </p>

            </article>

        `;


        try {

            const response =
                await fetch(
                    "/api/search",
                    {
                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json",

                            "Accept":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                query:
                                    query,

                                method:
                                    method.value,

                                top_k:
                                    5

                            })

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Search failed"
                );

            }


            displayResults(
                data
            );


        } catch (error) {

            console.error(
                "Knowledge search error:",
                error
            );


            resultsContainer.innerHTML = `

                <article class="knowledge-error-card">

                    <div class="knowledge-error-icon">

                        <i
                            data-lucide="alert-circle"
                        ></i>

                    </div>

                    <div>

                        <h3>
                            Search Error
                        </h3>

                        <p>
                            ${escapeHtml(
                                error.message
                            )}
                        </p>

                    </div>

                </article>

            `;


            status.textContent =
                "Search unavailable.";


            refreshIcons();


        } finally {

            button.disabled =
                false;


            button.classList.remove(
                "is-loading"
            );


            button.innerHTML = `

                <i
                    data-lucide="search"
                ></i>

                Search

            `;


            refreshIcons();

        }

    }


    /* =====================================================
       DISPLAY RESULTS
    ===================================================== */

    function displayResults(data) {

        const results =
            data.results || [];


        const selectedMethod =
            data.method ||
            method.value;


        status.innerHTML = `

            <span>
                Query
            </span>

            <strong>
                ${escapeHtml(
                    data.query || ""
                )}
            </strong>

            <span
                class="status-divider"
            >
                /
            </span>

            <span>
                Method
            </span>

            <strong>
                ${escapeHtml(
                    getMethodLabel(
                        selectedMethod
                    )
                )}
            </strong>

            <span
                class="status-divider"
            >
                /
            </span>

            <span>
                Results
            </span>

            <strong>
                ${results.length}
            </strong>

        `;


        if (!results.length) {

            resultsContainer.innerHTML = `

                <article
                    class="knowledge-empty-card"
                >

                    <div
                        class="knowledge-empty-icon"
                    >

                        <i
                            data-lucide="search-x"
                        ></i>

                    </div>

                    <h3>
                        No relevant documents found
                    </h3>

                    <p>
                        Try another HR-related query
                        or retrieval method.
                    </p>

                </article>

            `;


            refreshIcons();

            return;

        }


        resultsContainer.innerHTML =
            results.map(
                (result, index) => {

                    const score =
                        Number(
                            result.display_score ??
                            result.score ??
                            0
                        );


                    const matched =
                        result.matched_terms ||
                        [];


                    const documentName =
                        result.document ||
                        result.document_id ||
                        "Unknown document";


                    let documentId =
                        result.document_id ||
                        result.document ||
                        "Unknown";


                    /*
                     * The retrieval system may return
                     * a document name with .txt.
                     *
                     * Remove the extension before sending
                     * the identifier to the document API.
                     */

                    documentId =
                        String(
                            documentId
                        )
                        .replace(
                            /\.txt$/i,
                            ""
                        );


                    const rank =
                        index + 1;


                    return `

                        <article class="
                            knowledge-result-card
                            ${rank === 1
                                ? "top-result"
                                : ""}
                        ">


                            <!-- RESULT HEADER -->

                            <div class="
                                knowledge-result-header
                            ">

                                <div class="
                                    knowledge-result-rank
                                ">

                                    #${rank}

                                </div>


                                <div class="
                                    knowledge-result-title
                                ">

                                    <h3>

                                        ${escapeHtml(
                                            documentName
                                        )}

                                    </h3>


                                    <span>

                                        Document ID:

                                        ${escapeHtml(
                                            documentId
                                        )}

                                    </span>

                                </div>


                                <div class="
                                    knowledge-score
                                ">

                                    <small>
                                        Relevance
                                    </small>

                                    <strong>

                                        ${formatScore(
                                            score
                                        )}

                                    </strong>

                                </div>

                            </div>


                            <!-- METHOD -->

                            <div class="
                                knowledge-result-method
                            ">

                                <span>

                                    ${escapeHtml(
                                        getMethodLabel(
                                            selectedMethod
                                        )
                                    )}

                                </span>


                                <span class="
                                    result-rank-label
                                ">

                                    Rank ${rank}

                                </span>

                            </div>


                            <!-- MATCHED TERMS -->

                            ${
                                matched.length
                                ? `

                                    <div class="
                                        matched-terms-section
                                    ">

                                        <span>
                                            Matched terms
                                        </span>


                                        <div class="
                                            matched-terms
                                        ">

                                            ${matched
                                                .map(
                                                    term => `

                                                        <span
                                                            class="
                                                                matched-term
                                                            "
                                                        >

                                                            ${escapeHtml(
                                                                String(
                                                                    term
                                                                )
                                                            )}

                                                        </span>

                                                    `
                                                )
                                                .join("")
                                            }

                                        </div>

                                    </div>

                                `
                                : ""
                            }


                            <!-- VIEW DOCUMENT -->

                            <div
                                style="
                                    margin-top:18px;
                                    display:flex;
                                    justify-content:flex-end;
                                "
                            >

                                <button
                                    type="button"
                                    class="
                                        btn
                                        btn-primary
                                        view-document-btn
                                    "
                                    data-document-id="${escapeHtml(
                                        documentId
                                    )}"
                                >

                                    <i
                                        data-lucide="file-text"
                                    ></i>

                                    View Document

                                </button>

                            </div>


                        </article>

                    `;

                }
            ).join("");


        refreshIcons();

    }


    /* =====================================================
       OPEN DOCUMENT
    ===================================================== */

    async function openDocument(
        documentId
    ) {

        if (!documentId) {

            return;

        }


        createDocumentModal();


        const modal =
            document.getElementById(
                "documentModal"
            );

        const title =
            document.getElementById(
                "documentModalTitle"
            );

        const category =
            document.getElementById(
                "documentModalCategory"
            );

        const body =
            document.getElementById(
                "documentModalBody"
            );


        modal.style.display =
            "flex";


        title.textContent =
            "Loading document...";


        category.textContent =
            "";


        body.innerHTML = `

            <div
                style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    color:#94a3b8;
                "
            >

                <div
                    class="loading-ring"
                    style="
                        width:24px;
                        height:24px;
                    "
                ></div>

                <span>
                    Loading HR document...
                </span>

            </div>

        `;


        try {

            const response =
                await fetch(
                    `/api/document/${encodeURIComponent(
                        documentId
                    )}`,
                    {

                        method:
                            "GET",

                        headers: {
                            "Accept":
                                "application/json"
                        }

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Unable to load document"
                );

            }


            title.textContent =
                data.title ||
                documentId;


            category.textContent =
                data.category ||
                "HR Knowledge";


            body.textContent =
                data.content ||
                "Document content is empty.";


        } catch (error) {

            console.error(
                "Document retrieval error:",
                error
            );


            title.textContent =
                "Document unavailable";


            category.textContent =
                "";


            body.innerHTML = `

                <div
                    style="
                        padding:20px;
                        border:1px solid #7f1d1d;
                        background:#450a0a;
                        border-radius:10px;
                    "
                >

                    <div
                        style="
                            color:#fca5a5;
                            font-weight:600;
                            margin-bottom:8px;
                        "
                    >

                        Unable to open document

                    </div>


                    <div
                        style="
                            color:#fecaca;
                            font-size:12px;
                            line-height:1.6;
                        "
                    >

                        ${escapeHtml(
                            error.message
                        )}

                    </div>

                </div>

            `;

        }


        refreshIcons();

    }


    /* =====================================================
       CREATE DOCUMENT MODAL
    ===================================================== */

    function createDocumentModal() {

        if (
            document.getElementById(
                "documentModal"
            )
        ) {

            return;

        }


        const modal =
            document.createElement(
                "div"
            );


        modal.id =
            "documentModal";


        modal.style.cssText = `
            position:fixed;
            inset:0;
            z-index:99999;
            display:none;
            align-items:center;
            justify-content:center;
            padding:24px;
            background:rgba(2,6,23,.78);
            backdrop-filter:blur(6px);
        `;


        modal.innerHTML = `

            <div
                style="
                    width:min(
                        920px,
                        96vw
                    );
                    max-height:90vh;
                    display:flex;
                    flex-direction:column;
                    overflow:hidden;
                    background:#0f172a;
                    border:1px solid #1e293b;
                    border-radius:16px;
                    box-shadow:
                        0 25px 80px
                        rgba(0,0,0,.55);
                "
            >


                <!-- MODAL HEADER -->

                <div
                    style="
                        display:flex;
                        align-items:flex-start;
                        justify-content:space-between;
                        gap:16px;
                        padding:20px 22px;
                        border-bottom:1px solid #1e293b;
                    "
                >

                    <div>

                        <h2
                            id="documentModalTitle"
                            style="
                                margin:0;
                                color:#f8fafc;
                                font-size:18px;
                                font-weight:700;
                            "
                        >

                            HR Document

                        </h2>


                        <div
                            id="documentModalCategory"
                            style="
                                margin-top:6px;
                                color:#64748b;
                                font-size:11px;
                            "
                        >

                        </div>

                    </div>


                    <button
                        type="button"
                        id="closeDocumentModal"
                        aria-label="Close document"
                        style="
                            width:36px;
                            height:36px;
                            flex-shrink:0;
                            border:1px solid #334155;
                            background:#1e293b;
                            color:#cbd5e1;
                            border-radius:8px;
                            cursor:pointer;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                        "
                    >

                        <i
                            data-lucide="x"
                        ></i>

                    </button>

                </div>


                <!-- MODAL CONTENT -->

                <div
                    style="
                        flex:1;
                        overflow:auto;
                        padding:24px;
                    "
                >

                    <div
                        id="documentModalBody"
                        style="
                            color:#cbd5e1;
                            font-size:13px;
                            line-height:1.8;
                            white-space:pre-wrap;
                            word-break:break-word;
                            font-family:
                                Inter,
                                system-ui,
                                -apple-system,
                                BlinkMacSystemFont,
                                'Segoe UI',
                                sans-serif;
                        "
                    >

                        Loading HR document...

                    </div>

                </div>


                <!-- MODAL FOOTER -->

                <div
                    style="
                        display:flex;
                        justify-content:flex-end;
                        padding:14px 22px;
                        border-top:1px solid #1e293b;
                    "
                >

                    <button
                        type="button"
                        id="closeDocumentModalFooter"
                        class="btn btn-secondary"
                    >

                        Close

                    </button>

                </div>

            </div>

        `;


        document.body.appendChild(
            modal
        );


        const closeButton =
            document.getElementById(
                "closeDocumentModal"
            );


        const closeFooter =
            document.getElementById(
                "closeDocumentModalFooter"
            );


        closeButton.addEventListener(
            "click",
            closeDocumentModal
        );


        closeFooter.addEventListener(
            "click",
            closeDocumentModal
        );


        /*
         * Clicking the dark overlay closes
         * the document window.
         */

        modal.addEventListener(
            "click",
            event => {

                if (
                    event.target ===
                    modal
                ) {

                    closeDocumentModal();

                }

            }
        );


        refreshIcons();

    }


    /* =====================================================
       CLOSE DOCUMENT MODAL
    ===================================================== */

    function closeDocumentModal() {

        const modal =
            document.getElementById(
                "documentModal"
            );


        if (modal) {

            modal.style.display =
                "none";

        }

    }


    /* =====================================================
       VIEW DOCUMENT BUTTON EVENT
    ===================================================== */

    resultsContainer.addEventListener(
        "click",
        event => {

            const button =
                event.target.closest(
                    ".view-document-btn"
                );


            if (!button) {

                return;

            }


            const documentId =
                button.dataset.documentId;


            if (!documentId) {

                return;

            }


            openDocument(
                documentId
            );

        }
    );


    /* =====================================================
       QUICK SEARCH
    ===================================================== */

    quickSearchButtons.forEach(
        quickButton => {

            quickButton.addEventListener(
                "click",
                () => {

                    performSearch(
                        quickButton.dataset.query
                    );

                }
            );

        }
    );


    /* =====================================================
       EVENTS
    ===================================================== */

    button.addEventListener(
        "click",
        () => performSearch()
    );


    input.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter"
            ) {

                performSearch();

            }

        }
    );


    /* =====================================================
       ESCAPE KEY
    ===================================================== */

    document.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Escape"
            ) {

                closeDocumentModal();

            }

        }
    );


    /* =====================================================
       INITIAL STATE
    ===================================================== */

    updateMethodUI();

    refreshIcons();

});


/* =========================================================
   HELPERS
========================================================= */


/*
 * Format retrieval score.
 */

function formatScore(value) {

    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return "0.000";

    }


    return number.toFixed(3);

}


/*
 * Escape HTML safely.
 */

function escapeHtml(value) {

    return String(
        value ?? ""
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}