function getResults() {
  var results = $.ajax({
    type: "GET",
    url: "http://localhost:5000/hello",
    success: function() {
      alert("success");
    },
    error: function() {
      alert("didn't work :(");
    }
  })
}

function json2Table(json) {
  let cols = Object.keys(json[0]);

  //Map over columns, make headers, join to string
  let headerRow = createHeaderRowCols();
/*  let headerRow = cols
    .map(col => {`<th>${col}</th>`})
    .join("");
*/
  //map over array of json objs, for each row(obj) map over column values,
  //and return a td with the value of that object for its column
  //take that array of tds and join them
  //then return a row of the tds
  //finally join all the rows together
  let rows = json
    .map(row => {
      //let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
      let tds = createRowCols(row, cols);
      return `<tr>${tds}</tr>`;
    })
    .join("");

    const table = `
    	<table class="table table-striped table-hover" style="width:100%; margin-top:12px" id="dynamicTableTest">
    		<thead>
    			<tr>${headerRow}</tr>
    		</thead>
    		<tbody>
    			${rows}
    		</tbody>
    	</table>`;

    return table;
}

function createRowCols(row, cols) {
  let data = JSON.parse(JSON.stringify(row));
  return `
    <th id="headwordCol" scope="row">${data.headword}</th>
    <td id="quoteCol">${data.quote}</td>
    <td id="listTitleCol">${data.listTitle}</td>
    <td id="listAuthorCol">${data.listAuthor}</td>
    <td id="editionCol">${data.edition}</td>
    <td id="ratingCol">${data.rating}</td>
    <td id="flagCol"><input type="checkbox" id="bestFlag" name="bestFlag"></td>
    <td id="matchTitleCol">${data.matchTitle}</td>
    <td id="matchAuthorCol">${data.matchAuthor}</td>
    <td id="actualQuoteCol">${data.actualQuote}</td>
    <td id="urlCol">${data.url}</td>
  `
}

function createHeaderRowCols() {
  return `
  <th style="width:7.5%" id="headwordHeader">Headword</th>
  <th style="width:20%" id="quoteHeader">Quote</th>
  <th style="width:10%" id="listTitleHeader">Listed Title</th>
  <th style="width:7.5%" id="listAuthorHeader">Listed Author</th>
  <th style="width:2.5%" id="editionHeader">Ed.</th>
  <th style="width:5%" id="ratingHeader">Match Rating</th>
  <th style="width:2.5%" id="flagHeader">Mark best?</th>
  <th style="width:10%" id="matchTitleHeader">Matched Title</th>
  <th style="width:10%" id="matchAuthorHeader">Matched Author</th>
  <th style="width:20%" id="actualQuoteHeader">Actual Quote</th>
  <th style="width:5%" id="urlHeader">URL</th>
  `
}

function updateSearchOption(searchOption) {
    document.getElementById("chosenSearch").innerHTML = searchOption;
}


data = [{
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "KNOCK",
  "quote": "Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "listTitle": "Macbeth",
  "listAuthor": "Shak.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Macbeth",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.gutenberg.org/ebooks/1795"
}, {
  "headword": "MERMAID",
  "quote": "I'll drown more sailors than the mermaid shall.",
  "listTitle": "",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "The Works of William Shakespeare: King Henry VI, pt.1. King Henry VI, pt.2. King Henry VI, pt.3. King Richard III. King Henry VIII",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.google.com/books/edition/The_Works_of_William_Shakespeare_King_He/AC48AQAAIAAJ?hl=en&gbpv=0"
}, {
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "KNOCK",
  "quote": "Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "listTitle": "Macbeth",
  "listAuthor": "Shak.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Macbeth",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.gutenberg.org/ebooks/1795"
}, {
  "headword": "MERMAID",
  "quote": "I'll drown more sailors than the mermaid shall.",
  "listTitle": "",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "The Works of William Shakespeare: King Henry VI, pt.1. King Henry VI, pt.2. King Henry VI, pt.3. King Richard III. King Henry VIII",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.google.com/books/edition/The_Works_of_William_Shakespeare_King_He/AC48AQAAIAAJ?hl=en&gbpv=0"
}, {
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "KNOCK",
  "quote": "Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "listTitle": "Macbeth",
  "listAuthor": "Shak.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Macbeth",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.gutenberg.org/ebooks/1795"
}, {
  "headword": "MERMAID",
  "quote": "I'll drown more sailors than the mermaid shall.",
  "listTitle": "",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "The Works of William Shakespeare: King Henry VI, pt.1. King Henry VI, pt.2. King Henry VI, pt.3. King Richard III. King Henry VIII",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.google.com/books/edition/The_Works_of_William_Shakespeare_King_He/AC48AQAAIAAJ?hl=en&gbpv=0"
}, {
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "KNOCK",
  "quote": "Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "listTitle": "Macbeth",
  "listAuthor": "Shak.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Macbeth",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.gutenberg.org/ebooks/1795"
}, {
  "headword": "MERMAID",
  "quote": "I'll drown more sailors than the mermaid shall.",
  "listTitle": "",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "The Works of William Shakespeare: King Henry VI, pt.1. King Henry VI, pt.2. King Henry VI, pt.3. King Richard III. King Henry VIII",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.google.com/books/edition/The_Works_of_William_Shakespeare_King_He/AC48AQAAIAAJ?hl=en&gbpv=0"
}, {
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "KNOCK",
  "quote": "Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "listTitle": "Macbeth",
  "listAuthor": "Shak.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Macbeth",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.gutenberg.org/ebooks/1795"
}, {
  "headword": "MERMAID",
  "quote": "I'll drown more sailors than the mermaid shall.",
  "listTitle": "",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "The Works of William Shakespeare: King Henry VI, pt.1. King Henry VI, pt.2. King Henry VI, pt.3. King Richard III. King Henry VIII",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.google.com/books/edition/The_Works_of_William_Shakespeare_King_He/AC48AQAAIAAJ?hl=en&gbpv=0"
}, {
  "headword": "BITE",
  "quote": "Do you bite your tongue at me, sir?",
  "listTitle": "Romeo and Juliet",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Romeo and Juliet",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Do you bite your thumb at us, sir?",
  "url": "https://www.gutenberg.org/ebooks/1777"
}, {
  "headword": "KNOCK",
  "quote": "Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.Whence is that knocking? - How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "listTitle": "Macbeth",
  "listAuthor": "Shak.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "Macbeth",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.gutenberg.org/ebooks/1795"
}, {
  "headword": "MERMAID",
  "quote": "I'll drown more sailors than the mermaid shall.",
  "listTitle": "",
  "listAuthor": "Shakesp.",
  "edition": "1",
  "rating": "A",
  "flag": "[box]",
  "matchTitle": "The Works of William Shakespeare: King Henry VI, pt.1. King Henry VI, pt.2. King Henry VI, pt.3. King Richard III. King Henry VIII",
  "matchAuthor": "William Shakespeare",
  "actualQuote": "Whence is that knocking? How is't with me, when every noise appalls me? What hands are here! Ha, they pluck out mine eyes.",
  "url": "https://www.google.com/books/edition/The_Works_of_William_Shakespeare_King_He/AC48AQAAIAAJ?hl=en&gbpv=0"
}]

output = document.getElementById('testtable')
output.innerHTML = json2Table(data)
