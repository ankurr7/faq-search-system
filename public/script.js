async function search() {
    let q = document.getElementById("q").value;

    let res = await fetch("/search", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ query: q })
    });

    let data = await res.json();
    document.getElementById("ans").innerText = data.answer;
}
