function tf(words) {
    let freq = {};
    words.forEach(w => freq[w] = (freq[w] || 0) + 1);
    return freq;
}

function idf(docs) {
    let idf = {};
    let N = docs.length;

    docs.forEach(doc => {
        let unique = new Set(doc);
        unique.forEach(word => {
            idf[word] = (idf[word] || 0) + 1;
        });
    });

    Object.keys(idf).forEach(word => {
        idf[word] = Math.log(N / idf[word]);
    });

    return idf;
}

function tfidf(tf, idf) {
    let result = {};
    for (let word in tf) {
        result[word] = tf[word] * (idf[word] || 0);
    }
    return result;
}

module.exports = { tf, idf, tfidf };
