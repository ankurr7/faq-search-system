const express = require('express');
const fs = require('fs');

const tokenize = require('./utils/tokenizer');
const { tf, idf, tfidf } = require('./utils/tfidf');
const similarity = require('./utils/similarity');

const app = express();
app.use(express.json());
app.use(express.static('public'));

const faqs = JSON.parse(fs.readFileSync('faqs.json'));

app.post('/search', (req, res) => {
    let query = req.body.query;

    let queryWords = tokenize(query);
    let docs = faqs.map(f => tokenize(f.question));

    let idfValues = idf(docs);
    let queryVec = tfidf(tf(queryWords), idfValues);

    let best = null;
    let maxScore = -1;

    faqs.forEach((faq, i) => {
        let docVec = tfidf(tf(docs[i]), idfValues);
        let score = similarity(queryVec, docVec);

        if (score > maxScore) {
            maxScore = score;
            best = faq;
        }
    });

    if (maxScore < 0.1) {
        res.json({ answer: "No matching answer found ❌" });
    } else {
        res.json({ answer: best.answer });
    }
});

app.listen(3000, () => console.log("Running on http://localhost:3000"));
