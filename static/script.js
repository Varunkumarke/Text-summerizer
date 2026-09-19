// ========================================
// Word Count
// ========================================

function updateWordCount() {

    const text = document.getElementById("inputText").value.trim();

    const wordCount = text === ""
        ? 0
        : text.split(/\s+/).length;

    document.getElementById("wordCount").textContent =
        wordCount + (wordCount === 1 ? " word" : " words");
}


// ========================================
// Summarize Text
// ========================================

async function summarizeText() {

    const inputText = document.getElementById("inputText").value.trim();

    const output = document.getElementById("outputText");
    const status = document.getElementById("status");

    const button = document.getElementById("summarizeButton");
    const buttonText = document.getElementById("buttonText");

    // Check empty input
    if (inputText === "") {

        status.textContent = "Please enter some text first.";

        return;
    }


    // Loading state
    button.disabled = true;

    buttonText.textContent = "Summarizing...";

    status.textContent = "Generating your summary...";

    // Show loading animation in output area
    output.innerHTML = `
        <div class="loading-state">
            <div class="loader"></div>
            <p>Generating summary...</p>
            <span>Please wait while AI processes your text</span>
        </div>
    `;


    try {

        const response = await fetch("/predict?text=" + encodeURIComponent(inputText), {
            method: "POST"
        });


        if (!response.ok) {

            throw new Error("Failed to generate summary.");
        }


        const summary = await response.text();


        // Display summary
        output.innerHTML = "";

        output.textContent = summary;


        // Update summary word count
        const summaryWords = summary.trim() === ""
            ? 0
            : summary.trim().split(/\s+/).length;

        document.getElementById("summaryWordCount").textContent =
            summaryWords +
            (summaryWords === 1 ? " word" : " words");


        status.textContent = "Summary generated successfully.";


    } catch (error) {

        console.error(error);

        output.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">⚠️</div>
                <p>Something went wrong</p>
                <span>Could not generate the summary.</span>
            </div>
        `;

        status.textContent = "Error generating summary.";


    } finally {

        // Restore button
        button.disabled = false;

        buttonText.textContent = "Summarize";
    }
}


// ========================================
// Copy Summary
// ========================================

async function copySummary() {

    const output = document.getElementById("outputText");

    const summary = output.textContent.trim();


    if (summary === "") {

        return;
    }


    try {

        await navigator.clipboard.writeText(summary);

        document.getElementById("status").textContent =
            "Summary copied to clipboard.";

    } catch (error) {

        console.error(error);

        document.getElementById("status").textContent =
            "Could not copy the summary.";
    }
}


// ========================================
// Clear Input
// ========================================

function clearText() {

    document.getElementById("inputText").value = "";

    document.getElementById("outputText").innerHTML = `
        <div class="empty-state">

            <div class="empty-icon">
                ✨
            </div>

            <p>
                Your summary will appear here
            </p>

            <span>
                Enter some text and click Summarize
            </span>

        </div>
    `;

    document.getElementById("wordCount").textContent =
        "0 words";

    document.getElementById("summaryWordCount").textContent =
        "0 words";

    document.getElementById("status").textContent = "";
}


// ========================================
// Load Example
// ========================================

function loadExample() {

    const example = `Amanda: I cannot find Betty's phone number.
Larry: I talked to Betty at the park yesterday.
Hannah: Amanda should text Larry and ask for Betty's number.`;

    document.getElementById("inputText").value = example;

    updateWordCount();

    document.getElementById("status").textContent =
        "Example conversation loaded.";
}