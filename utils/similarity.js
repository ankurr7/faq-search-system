function similarity(v1, v2) {
    let score = 0;
    for (let word in v1) {
        if (v2[word]) {
            score += v1[word] * v2[word];
        }
    }
    return score;
}
module.exports = similarity;
