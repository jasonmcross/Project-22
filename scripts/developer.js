const submitDesignProblem = document.getElementById("problem-form");
const goToLogin = document.getElementById("admin-login");

submitDesignProblem.addEventListener("click", submitDesignProblemScript);
goToLogin.addEventListener("click", goToLoginScript);

function submitDesignProblemScript(event) {
    const problem = document.getElementById("design-problem").value;
    var collection = document.getElementById("collection-select").value;
    var source = document.getElementById("library-select").value;

    // 0 indicates that no collection was selected
    if (collection <= 0) {
        return;
    }
    else {
        // Converts entered design problem into json format
        var message = JSON.stringify(problem);

        // Send message to machine learning to convert into vector
        var problemVector = [];

        // Request data from database for entered collection and limit by library source
        var collectionPatternNames = [];
        var collectionPatternVectors = [0][0];

        // Calculates cosine similarity scores between the design problem vector and each design pattern vector
        var cosineScores = [];

        for (var i = 0; i < collectionPatternVectors.length; i++) {
            cosineScores[i] = cosineSimilarity(problemVector, collectionPatternVectors[i]);
        }

        // Displays list that consists of all design patterns and their cosine similarity scores to html
        for (var i = 0; i < cosineScores.length; i++) {
            document.getElementById("pattern-list").innerHTML += ('<li>' + 'Design Pattern: ' + collectionPatternNames[i] + '&emsp' + 'Cosine Similarity Score: ' + cosineScores[i]);
        }
    }
}
function goToLoginScript(event) {
    // Put admin login page URL here
    window.location.replace("../newpages/admin-login.html");
}

// Calculates the cosine similarity between two vectors represented as arrays
function cosineSimilarity(a1, a2) {
    var dot = 0; // Dot product
    var a1Magnitude = 0; // Magnitude of first array
    var a2Magnitude = 0; // Magnitude of second array

    // Finds dot product and adds square of each element to a1/a2 magnitude
    for (var index = 0; index < a1.length; index++) {
        a1Magnitude += a1[index] * a1[index];
        a2Magnitude += a2[index] * a2[index];
        dot += a1[index] * a2[index]
    }
    // Final step to find magnitude for a1 and a2
    a1Magnitude = Math.sqrt(a1Magnitude);
    a2Magnitude = Math.sqrt(a2Magnitude);

    // Calculates cosine similarity
    var result = dot / (a1Magnitude * a2Magnitude);

    return result;
}
