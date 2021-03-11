function getResults() {
  var arr = { author: "shakespeare"}
  jQuery.support.cors = true;
  var results = $.ajax({
    type: "GET",
    url: "http://localhost:5000/get_matches_by_headword",
    dataType: "json",
    contentType: 'application/json; charset=utf-8',
    success: function() {
      console.log(arguments);
    },
    error: function() {
      console.log(arguments);
    }
  })
}

$("#loginForm").submit(function() {
  var username = $("#username").val();
  var password = $("#password").val();
  alert(username);
  $.ajax({
    type: "GET",
    url: "http://localhost:5000/hello",
    dataType: "json",
    success: function(){
      console.log("success!");
      console.log(arguments);
    },
    error: function(){
      console.log(arguments);
    }
  })

});

$("#testbutton").click(function() {

  $.ajax({
    type: "GET",
    url: "php/hello.php",
    dataType: "json",
    success: function(data){
      console.log("success!");
      console.log(data);
    },
    error: function(data){
      console.log(data);
    }
  })

});

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
    <td id="ratingCol">${data.score}</td>
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

function json2Table2(json) {
  let cols = Object.keys(json[0]);

  //Map over columns, make headers, join to string
  let headerRow = createQuoteHeaderRowCols();
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
      let tds = createQuoteRowCols(row, cols);
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

function createQuoteHeaderRowCols() {
  return `
  <th style="width:16%" id="headwordHeader">Headword</th>
  <th style="width:16%" id="quoteHeader">Quote</th>
  <th style="width:16%" id="quoteTitleHeader">Listed Title</th>
  <th style="width:16%" id="quoteAuthorHeader">Listed Author</th>
  <th style="width:16%" id="editionHeader">Ed.</th>
  `
  //<th style="width:16%" id="quoteIDHeader">Quote ID</th>
}

function createQuoteRowCols(row, cols) {
  let data = JSON.parse(JSON.stringify(row));
  // Initialize matches to empty array to avoid parsing "undefined"
  var matches = [];
  var edition;
  if (data.edition == "both") {
    data.edition = "1/4"
  }

  if (Object.keys(data.matches).length > 0) {
    matches = createMatchTable(data.matches);
  }
  return `
    <th id="headwordCol" scope="row">${data.headword}</th>
    <td id="quoteCol">${data.content}</td>
    <td id="quoteTitleCol">${data.title}</td>
    <td id="quoteAuthorCol">${data.author}</td>
    <td id="editionCol">${data.edition}</td>
    ${matches}
  `
  //<td id="quoteIDCol">${data.quote_id}</td>
}

function createMatchTable(matchArr) {
  let cols = Object.keys(matchArr[0]);
  let headerRow = createMatchHeaderRowCols();

  let rows = matchArr
    .map(row => {
      //let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
      let tds = createMatchRowCols(row, cols);
      return `<tr>${tds}</tr>`;
    })
    .join("");

  // Note: no tbody tags needed; Boostrap generates tbody tags around tr tags.
  return `
    <tr>
      <td colspan="5">
        <table id="matchTable" class="table table-bordered table-striped">
          <thead>
          <tr>
            ${headerRow}
          </tr>
          </thead>
            ${rows}
        </table>
      </td>
    </tr>
    `
}

function createMatchHeaderRowCols() {
  return `
  <th style="width:14%" id="scoreHeader">Match Rating</th>
  <th style="width:14%" id="matchQuoteHeader">Sourced Quote</th>
  <th style="width:14%" id="matchTitleHeader">Title</th>
  <th style="width:14%" id="matchAuthorHeader">Author</th>
  <th style="width:14%" id="flagHeader">Mark best?</th>
  <th style="width:25%" id="urlHeader">URL to Source</th>
  `
  //<th style="width:14%" id="matchIDHeader">Match ID</th>
}

function createMatchRowCols(row, cols) {
  let data = JSON.parse(JSON.stringify(row));
  var markedBest = "";
  if (data.flag) {
    markedBest = "checked";
  }
  return `
    <th id="ratingCol" scope="row">${data.score}</th>
    <td id="matchQuoteCol">${data.content}</td>
    <td id="matchTitleCol">${data.title}</td>
    <td id="matchAuthorCol">${data.author}</td>
    <td id="flagCol"><input type="checkbox" id="bestFlag" name="bestFlag" ${markedBest}></td>
    <td id="urlCol">${data.url}</td>
  `
  //<td id="matchIDCol">${data.matchID}</td>
}

function updateSearchOption(searchOption) {
  $("#chosenSearchOption").attr("value", searchOption);
    switch(searchOption) {
      case ('get_matches_by_headword'):
        $("#chosenSearch").html("Matches by Headword");
        break;
      case ("get_matches_by_author"):
        $("#chosenSearch").html("Matches by Author");
        break;
      case ("get_matches_by_title"):
        $("#chosenSearch").html("Matches by Title");
        break;
      case ("get_matches_by_random"):
        $("#chosenSearch").html("Random Selection");
        break;
    }
}

var data3 = [
   {
      "author": "Bible",
      "content": "Ye shall flee when none pursueth you.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Various",
            "best_match": false,
            "content": ":36 And upon them that are left alive of you I will send a faintness\n      into their hearts in the lands of their enemies; and the sound of a shaken\n      leaf shall chase them; and they shall flee, as fleeing from a sword; and\n      they shall fall when none pursueth.\n    \n\n      26",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 84.058,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ": they that hate you shall reign over you; and ye shall flee\n      when none pursueth you",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 81.6901,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": they that hate you shall reign over you; and ye shall\nflee when none pursueth you",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4521,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":36 And upon them that are left alive of you I will send a faintness\ninto their hearts in the lands of their enemies; and the sound of a\nshaken leaf shall chase them; and they shall flee, as fleeing from a\nsword; and they shall fall when none pursueth",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4521,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": they that hate you shall reign over you; and ye shall\nflee when none pursueth you.\n26:18 And if ye will not yet for all this hearken unto me, then I will\npunish you seven times more for your sins",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 71.2329,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 96659,
      "title": "Lev."
   },
   {
      "author": "Wilk.",
      "content": "That fowl which is none of the lightest, can easily move itself up and down in the air without stirring its wings.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 90313,
      "title": ""
   },
   {
      "author": "Addison\u2019s",
      "content": "Another, which is none of the least advantages of hope is, its great efficacy in preserving us from setting too high a value on present enjoyments.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 44446,
      "title": "Spectator."
   },
   {
      "author": "Bible",
      "content": "Six days shall ye gather it, but on the sabbath there shall be none.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Various",
            "best_match": false,
            "content": ":26 Six days ye shall gather it; but on the seventh day, which is the\n      sabbath, in it there shall be none",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 69.697,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":1 Thus saith the Lord GOD; The gate of the inner court that looketh\ntoward the east shall be shut the six working days; but on the sabbath\nit shall be opened, and in the day of the new moon it shall be opened",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 66.6667,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ".\n35:2 Six days shall work be done, but on the seventh day there shall\nbe to you an holy day, a sabbath of rest to the LORD",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 66.1654,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": to day ye shall not find it in the field.\n16:26 Six days ye shall gather it; but on the seventh day, which is\nthe sabbath, in it there shall be none",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 65.1852,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":7 And two parts of all you that go forth on the sabbath, even they\nshall keep the watch of the house of the LORD about the king",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 64.1791,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 2958,
      "title": "Exodus"
   },
   {
      "author": "Bible",
      "content": "Thy life shall hang in doubt, and shalt have none assurance of this life.",
      "edition": "1",
      "headword": "NONE",
      "matches": [
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":66 And\nthy life shall hang in doubt before thee; and thou shalt fear day and\nnight, and shalt have none assurance of thy life: 28",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.4828,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":66 And thy life shall hang in doubt before thee; and thou shalt fear\n      day and night, and shalt have none assurance of thy life:\n    \n\n      28:67 In the morning thou shalt say, Would God it were even",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 68.0556,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":66 And thy life shall hang in doubt before thee; and thou shalt fear\n      day and night, and shalt have none assurance of thy life",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 63.4483,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":23 And when ye shall come into the land, and shall have planted all\nmanner of trees for food, then ye shall count the fruit thereof as\nuncircumcised",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 62.069,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":14 And the LORD God said unto the serpent, Because thou hast done this,\n      thou art cursed above all cattle, and above every beast of the field; upon\n      thy belly shalt thou go, and dust shalt thou eat all the days of thy life",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 60.6897,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         }
      ],
      "quote_id": 11694,
      "title": "Deutr."
   },
   {
      "author": "Burnet\u2019s",
      "content": "Before the deluge, the air was calm; none of those tumultuary motions of vapours, which the mountains and winds cause in ours.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 101196,
      "title": "Theory of the Earth."
   },
   {
      "author": "Fenton",
      "content": "The most glaring and notorious passages, are none of the finest.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 25824,
      "title": "on the Classicks."
   },
   {
      "author": "Bible",
      "content": "This is none other but the house of God, and the gate of heaven.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": "! this is\nnone other but the house of God, and this is the gate of heaven",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 88.189,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":17 And he was afraid, and said, How dreadful is this place! this is\n      none other but the house of God, and this is the gate of heaven",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 77.1654,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":31 And the children of Benjamin went out against the people, and\nwere drawn away from the city; and they began to smite of the people,\nand kill, as at other times, in the highways, of which one goeth up to\nthe house of God, and the other to Gibeah in the field, about thirty\nmen of Israel",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 69.8413,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": for the LORD had made them joyful, and turned the heart of the\nking of Assyria unto them, to strengthen their hands in the work of\nthe house of God, the God of Israel",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 67.7165,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ".\n    \n\n      36:19 And they burnt the house of God, and brake down the wall of\n      Jerusalem, and burnt all the palaces thereof with fire, and destroyed all\n      the goodly vessels thereof",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 67.2414,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         }
      ],
      "quote_id": 32470,
      "title": "Gen."
   },
   {
      "author": "Bible",
      "content": "My people would not hearken to my voice: and Israel would none of me.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Various",
            "best_match": false,
            "content": ".\n    \n\n      81:11 But my people would not hearken to my voice; and Israel would none\n      of me",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 84.4444,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": open thy mouth wide, and I will fill it.\n81:11 But my people would not hearken to my voice; and Israel would\nnone of me",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4118,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":11 But my people would not hearken to my voice; and Israel would\nnone of me.\n81:12 So I gave them up unto their own hearts\u2019 lust",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 70.5882,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":11 But my people would not hearken to my voice; and Israel would none\n      of me.\n    \n\n      81:12 So I gave them up unto their own hearts' lust",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 65.6934,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":13 Therefore it is come to pass, that as he cried, and they would\nnot hear; so they cried, and I would not hear, saith the LORD of\nhosts",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 62.7737,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 9476,
      "title": "Ps."
   },
   {
      "author": "Bible",
      "content": "Ye shall flee when none pursueth you.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Various",
            "best_match": false,
            "content": ":36 And upon them that are left alive of you I will send a faintness\n      into their hearts in the lands of their enemies; and the sound of a shaken\n      leaf shall chase them; and they shall flee, as fleeing from a sword; and\n      they shall fall when none pursueth.\n    \n\n      26",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 84.058,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ": they that hate you shall reign over you; and ye shall flee\n      when none pursueth you",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 81.6901,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": they that hate you shall reign over you; and ye shall\nflee when none pursueth you",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4521,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":36 And upon them that are left alive of you I will send a faintness\ninto their hearts in the lands of their enemies; and the sound of a\nshaken leaf shall chase them; and they shall flee, as fleeing from a\nsword; and they shall fall when none pursueth",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4521,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": they that hate you shall reign over you; and ye shall\nflee when none pursueth you.\n26:18 And if ye will not yet for all this hearken unto me, then I will\npunish you seven times more for your sins",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 71.2329,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 96659,
      "title": "Lev."
   },
   {
      "author": "Carew.",
      "content": "That killing power is none of thine, I gave it to thy voice and eyes: Thy sweets, thy graces, all are mine; Thou art my star, shin\u2019st in my skies.",
      "edition": "4",
      "headword": "NONE",
      "matches": [],
      "quote_id": 112102,
      "title": ""
   },
   {
      "author": "Wilkins.",
      "content": "That fowl which is none of the lightest, can easily move itself up and down in the air without stirring its wings.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 90313,
      "title": ""
   },
   {
      "author": "Addison\u2019s",
      "content": "Another, which is none of the least advantages of hope is, its great efficacy in preserving us from setting too high a value on present enjoyments.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 44446,
      "title": "Spectator."
   },
   {
      "author": "Bible",
      "content": "Six days shall ye gather it, but on the sabbath there shall be none.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Various",
            "best_match": false,
            "content": ":26 Six days ye shall gather it; but on the seventh day, which is the\n      sabbath, in it there shall be none",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 69.697,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":1 Thus saith the Lord GOD; The gate of the inner court that looketh\ntoward the east shall be shut the six working days; but on the sabbath\nit shall be opened, and in the day of the new moon it shall be opened",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 66.6667,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ".\n35:2 Six days shall work be done, but on the seventh day there shall\nbe to you an holy day, a sabbath of rest to the LORD",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 66.1654,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": to day ye shall not find it in the field.\n16:26 Six days ye shall gather it; but on the seventh day, which is\nthe sabbath, in it there shall be none",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 65.1852,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":7 And two parts of all you that go forth on the sabbath, even they\nshall keep the watch of the house of the LORD about the king",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 64.1791,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 2958,
      "title": "Exodus"
   },
   {
      "author": "Bible",
      "content": "Thy life shall hang in doubt, and thou shalt have none assurance of this life.",
      "edition": "4",
      "headword": "NONE",
      "matches": [
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":66 And\nthy life shall hang in doubt before thee; and thou shalt fear day and\nnight, and shalt have none assurance of thy life",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 67.0968,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":\n    \n\n      28:66 And thy life shall hang in doubt before thee; and thou shalt fear\n      day and night, and shalt have none assurance of thy life",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 64.8649,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":66 And\nthy life shall hang in doubt before thee; and thou shalt fear day and\nnight, and shalt have none assurance of thy life",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 64.5161,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":66 And thy life shall hang in doubt before thee; and thou shalt fear\n      day and night, and shalt have none assurance of thy life:\n    \n\n      28:67 In the morning thou shalt say, Would God it were even",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 63.2258,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": thy sheep shall be given unto\nthine enemies, and thou shalt have none to rescue them.\n28",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 62.3377,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 63089,
      "title": "Deut."
   },
   {
      "author": "Burnet\u2019s",
      "content": "Before the deluge, the air was calm; none of those tumultuary motions of vapours, which the mountains and winds cause in ours.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 101196,
      "title": "Theory."
   },
   {
      "author": "Felton",
      "content": "The most glaring and notorious passages, are none of the finest.",
      "edition": "both",
      "headword": "NONE",
      "matches": [],
      "quote_id": 25824,
      "title": "on the Classicks."
   },
   {
      "author": "Bible",
      "content": "This is none other but the house of God, and the gate of heaven.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": "! this is\nnone other but the house of God, and this is the gate of heaven",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 88.189,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":17 And he was afraid, and said, How dreadful is this place! this is\n      none other but the house of God, and this is the gate of heaven",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 77.1654,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":31 And the children of Benjamin went out against the people, and\nwere drawn away from the city; and they began to smite of the people,\nand kill, as at other times, in the highways, of which one goeth up to\nthe house of God, and the other to Gibeah in the field, about thirty\nmen of Israel",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 69.8413,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": for the LORD had made them joyful, and turned the heart of the\nking of Assyria unto them, to strengthen their hands in the work of\nthe house of God, the God of Israel",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 67.7165,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ".\n    \n\n      36:19 And they burnt the house of God, and brake down the wall of\n      Jerusalem, and burnt all the palaces thereof with fire, and destroyed all\n      the goodly vessels thereof",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 67.2414,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         }
      ],
      "quote_id": 32470,
      "title": "Gen."
   },
   {
      "author": "Bible",
      "content": "My people would not hearken to my voice: and Israel would none of me.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Various",
            "best_match": false,
            "content": ".\n    \n\n      81:11 But my people would not hearken to my voice; and Israel would none\n      of me",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 84.4444,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ": open thy mouth wide, and I will fill it.\n81:11 But my people would not hearken to my voice; and Israel would\nnone of me",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4118,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":11 But my people would not hearken to my voice; and Israel would\nnone of me.\n81:12 So I gave them up unto their own hearts\u2019 lust",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 70.5882,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         },
         {
            "author": "Various",
            "best_match": false,
            "content": ":11 But my people would not hearken to my voice; and Israel would none\n      of me.\n    \n\n      81:12 So I gave them up unto their own hearts' lust",
            "filepath": "gut_texts/gut13563The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 65.6934,
            "title": "The King James Bible, Complete",
            "url": "https://www.gutenberg.org/files/10900/10900-h/10900-h.htm"
         },
         {
            "author": "UNKNOWN Author",
            "best_match": false,
            "content": ":13 Therefore it is come to pass, that as he cried, and they would\nnot hear; so they cried, and I would not hear, saith the LORD of\nhosts",
            "filepath": "gut_texts/gut7098The-K.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 62.7737,
            "title": "The King James Bible",
            "url": "https://www.gutenberg.org/files/10/10-h/10-h.htm"
         }
      ],
      "quote_id": 9476,
      "title": "Ps."
   },
   {
      "author": "Milton.",
      "content": "Terms of peace were none  Vouchsaf\u2019d.",
      "edition": "4",
      "headword": "NONE",
      "matches": [
         {
            "author": "Milton, John, 1608-1674, Tonson, Jacob, 1656?-1736,, Fenton, Elijah, 1683-1730",
            "best_match": false,
            "content": ":\nWar hath determin'd us, and foil'd with loſs\n32 f\n330\nIrreparable; terms of peace yet none .\nVouchſaf'd or ſought",
            "filepath": "hat_texts/hat4804Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 82.1918,
            "title": "Paradise lost. : A poem, in twelve books / The author John Milton",
            "url": "https://catalog.hathitrust.org/Record/009774431?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Milton, John, 1608-1674., Hayman, Francis, 1708-1776., Miller, John, 1715-1790?, Vertue, George, 1684-1756.",
            "best_match": false,
            "content": "? \n \n War hath determin\u2019d us, and foil\u2019d with lofs 33d \n Irreparable ; terms of peace yet none \n Vouchfaf\u2019d or fought ; for what peace will be given \n To us inflav\u2019d, but cuftody fevere",
            "filepath": "hat_texts/hat9127Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 80.5556,
            "title": "Paradise lost : a poem, in twelve books / the author John Milton.",
            "url": "https://catalog.hathitrust.org/Record/102129933?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Milton, John, 1608-1674., Smith, W., (Dublin), Ewing, G., (Dublin), Risk, G., (Dublin), Powell, S., (Dublin)",
            "best_match": false,
            "content": "?\nWar hath determin'd us, and foild with loſs 33\nIrreparable; terms of peace yet none\nVouchſafd or ſought",
            "filepath": "hat_texts/hat9744Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 79.4521,
            "title": "Paradise lost : a poem, in twelve books / the author John Milton.",
            "url": "https://catalog.hathitrust.org/Record/009337696?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "John Milton",
            "best_match": false,
            "content": ": 330\nIrreparable; tearms of peace yet none\nVoutsaf\u2019t or sought; for what peace will be giv\u2019n\nTo us enslav\u2019d, but custody severe,\nAnd stripes, and arbitrary punishment\nInflicted",
            "filepath": "lib_texts/lib1384The-P.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 73.9726,
            "title": "The Poetical Works of John Milton",
            "url": "https://oll.libertyfund.org/title/milton-the-poetical-works-of-john-milton#preview"
         },
         {
            "author": "Milton, John, 1608-1674., Newton, Thomas, 1704-1782., J. and R. Tonson.",
            "best_match": false,
            "content": "?\nWar hath determin\u2019d us, and foild with loſs 330\nIrreparable; terms of peace yet none\nVouchſaf\u2019d or ſought; for what peace will be given\nTo us inflay'd, but cuſtody ſevere,\n",
            "filepath": "hat_texts/hat2145Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 73.9726,
            "title": "Paradise lost : a poem in twelve books / the author John Milton.",
            "url": "https://catalog.hathitrust.org/Record/008627866?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         }
      ],
      "quote_id": 118690,
      "title": ""
   },
   {
      "author": "Milton.",
      "content": "In at this gate none pass The vigilance here plac\u2019d, but such as come Well known from heav\u2019n.",
      "edition": "both",
      "headword": "NONE",
      "matches": [
         {
            "author": "Milton, John, 1608-1674., Smith, W., (Dublin), Ewing, G., (Dublin), Risk, G., (Dublin), Powell, S., (Dublin)",
            "best_match": false,
            "content": "! no wonder if thy perfect fight,\nAmid the \u017fun's bright circle, where thou fit'\u017ft,\nSee far, and wide; in at this gate none pafs\nThe vigilance here plac'd, but ſuch as come\nWell-known from heav'n; and fince meridian hour\nNo creature thence",
            "filepath": "hat_texts/hat9744Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 97.8261,
            "title": "Paradise lost : a poem, in twelve books / the author John Milton.",
            "url": "https://catalog.hathitrust.org/Record/009337696?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Milton, John, 1608-1674., Hawkey, John, 1703-1759,",
            "best_match": false,
            "content": ": in at this gate none paſs\nThe vigilance here plac'd, but ſuch as come 580\nWell known from heav'n; and ſince meridian hour\nNo creature thence",
            "filepath": "hat_texts/hat2061Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 88.0435,
            "title": "Paradise lost : a poem, in twelve books / the author John Milton ; compared with the authentic editions and revised by John Hawkey, editor of the Latin classics.",
            "url": "https://catalog.hathitrust.org/Record/008401574?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "John Milton",
            "best_match": false,
            "content": ": in at this Gate none pass\nThe vigilance here plac\u2019t, but such as come\nWell known from Heav\u2019n; and since Meridian hour\nNo Creature thence",
            "filepath": "gut_texts/gut36907Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 85.4054,
            "title": "Paradise Lost",
            "url": "https://www.gutenberg.org/files/20/20-h/20-h.htm"
         },
         {
            "author": "Milton, John, 1608-1674., Hume, Patrick, fl. 1695.",
            "best_match": false,
            "content": ". In at this Gate none paſs\nThe vigilance here plac'd, but ſuch as come 580\nWell known from Heav'n; and ſince Meridian hour\nNo Creature thence",
            "filepath": "hat_texts/hat2056The-p.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 85.4054,
            "title": "The poetical works of Mr. John Milton.",
            "url": "https://catalog.hathitrust.org/Record/008399493?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Milton, John, 1608-1674., Hayman, Francis, 1708-1776., Miller, John, 1715-1790?, Vertue, George, 1684-1756.",
            "best_match": false,
            "content": ". \n \n Amid the fun\u2019s bright circle where thou fitfl, \n \n See far and wide : in at this gate none pafs \n The vigilance here plac\u2019d, but fuch as come 58® \n Well known from Heav\u2019n ; and fince meridian hour \n No creature thence ",
            "filepath": "hat_texts/hat9127Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 83.2432,
            "title": "Paradise lost : a poem, in twelve books / the author John Milton.",
            "url": "https://catalog.hathitrust.org/Record/102129933?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         }
      ],
      "quote_id": 11759,
      "title": ""
   },
   {
      "author": "Milton.",
      "content": "Nor think though men were none  That heav\u2019n would want spectators, God want praise.",
      "edition": "4",
      "headword": "NONE",
      "matches": [
         {
            "author": "Milton, John, 1608-1674., Hume, Patrick, fl. 1695.",
            "best_match": false,
            "content": ".\nShine not in vain; nor think, though men were none,\nThat Heav'n would want ſpectators, God want praiſe;\nMillions of ſpiritual Creatures walk the Earth\nUnſeen, both when we wake, and when we ſleep",
            "filepath": "hat_texts/hat2056The-p.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 92.6829,
            "title": "The poetical works of Mr. John Milton.",
            "url": "https://catalog.hathitrust.org/Record/008399493?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "John Milton",
            "best_match": false,
            "content": ".\nThese then, though unbeheld in deep of night,\nShine not in vain, nor think, though men were none,\nThat heav\u2019n would want spectators, God want praise;\nMillions of spiritual Creatures walk the Earth\nUnseen, both when we wake, and when we sleep",
            "filepath": "lib_texts/lib1384The-P.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 90.9091,
            "title": "The Poetical Works of John Milton",
            "url": "https://oll.libertyfund.org/title/milton-the-poetical-works-of-john-milton#preview"
         },
         {
            "author": "Milton, John, 1608-1674., Hayman, Francis, 1708-1776., Miller, John, 1715-1790?, Vertue, George, 1684-1756.",
            "best_match": false,
            "content": ". \n \n Thefe then, though unbeheld in deep of night, 6y^\u2019 \n Shine not in vain ; nor think, though men were none. \n That Heav\u2019n would want fpedators, God want praife : \n Millions of fpiritual creatures walk the earth \n Unfeen, both when we wake, and when we fleep ",
            "filepath": "hat_texts/hat9127Parad.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 84.8485,
            "title": "Paradise lost : a poem, in twelve books / the author John Milton.",
            "url": "https://catalog.hathitrust.org/Record/102129933?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "John Milton",
            "best_match": false,
            "content": ".\n  These then, though unbeheld in deep of night,\n  Shine not in vain, nor think, though men were none,\n  That heav'n would want spectators, God want praise;\n  Millions of spiritual Creatures walk the Earth\n  Unseen, both when we wake, and when we sleep",
            "filepath": "gut_texts/gut15066The-P.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 83.6364,
            "title": "The Poetical Works of John Milton",
            "url": "https://www.gutenberg.org/files/1745/1745-h/1745-h.htm"
         },
         {
            "author": "Milton, John, 1608-1674.",
            "best_match": false,
            "content": ". Theſe\nthen, though not ſeen in the Dead of Night, do yet not\nſhine in vain; nor let us think though there were no\nMen, that Heaven would want Spectators, or God\nwant Praiſe ; for there are Millions of ſpiricual Crea-\ntures, that unſeen walk the Earth, both when we are\nawake and when we ſeep; all theſe with never cea-\nſing Praiſe behold his Works, both Day and Night",
            "filepath": "hat_texts/hat2907Milto.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 83.2298,
            "title": "Milton's Paradise lost; or, The fall of man, with historical, philosophical, critical, and explanatory notes, from ... Raymond de St. Maur ... in twelve books.",
            "url": "https://catalog.hathitrust.org/Record/008394836?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         }
      ],
      "quote_id": 33773,
      "title": ""
   },
   {
      "author": "Bentley\u2019s",
      "content": "When they say nothing from nothing, they must understand it as excluding all causes. In which sense it is most evidently true; being equivalent to this proposition, that nothing can make itself, or, nothing cannot bring its no-self out of nonentity into something.",
      "edition": "both",
      "headword": "NONENTITY",
      "matches": [
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". For\nwhen they fay, Nothing from Nothing5 they must\nso understand it, as excluding all Causes, both ma-\nterial and efficient. In which fense it is most evi-\ndently and infallibly true: being equivalent to this\nproposition 5 that Nothing can make it self, or,\nNothing cannot bring its no self out of non-entity\ninto Something",
            "filepath": "hat_texts/hat977The-f.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 78.4762,
            "title": "The folly and unreasonableness of atheism demonstrated from the advantage and pleasure of a religious life, the faculties of humane souls, the structure of animate bodies, & the...",
            "url": "https://catalog.hathitrust.org/Record/001925709?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". For when they ſay,\nNothing from Nothing ; they muſt ſo underſtand it, as\nexcluding all Cauſes, both material and efficient. In\nwhich ſenſe it is moſt evidently and infallibly true: be-\ning equivalent to this propoſition; that nothing can\nmake it ſelf, or, Nothing cannot bring its no-ſelf out of\nnon-entity into Something",
            "filepath": "hat_texts/hat5601The-f.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 77.0398,
            "title": "The folly and unreasonableness of atheism : demonstrated from the advantage and pleasure of a religious life, the faculties of human souls, the structure of animate bodies, &...",
            "url": "https://catalog.hathitrust.org/Record/100170743?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". For when they ſay, Nothing from No-\nthing ; they muſt ſo underſtand it, as excluding all\nCauſes, both material and efficient. In which\nfence it is moſt evidently and infallibly true: be.\ning equivalent to this propoſition; that nothing can\nmake it ſelf, or, Nothing cannot bring its no-ſelf\nout of non enticy into Something",
            "filepath": "hat_texts/hat1027The-f.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.3833,
            "title": "The folly and unreasonableness of atheism ... in eight sermons preached at the lecture founded by the Honourable Robert Boyle, esquire; in the first year MDCXCII.",
            "url": "https://catalog.hathitrust.org/Record/001925703?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". of ATHEISM. 239\nwhen they fay, Nothing from Nothing;\nthey muſt ſo underſtand it, as excluding\nall Cauſes, both material and efficient.\nIn which fenſe it is moſt evidently and\ninfallibly true: being equivalent to this\npropoſition; that Nothing can make it\nJelf, or, Nothing cannot bring its no-\nfelf out of non-entity into Something",
            "filepath": "hat_texts/hat10912Eight.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.0038,
            "title": "Eight sermons preach'd at the Honourable Robert Boyle's lecture, in the first year, MDCXCII. 5th ed., to which is now added a sermon preach'd at the Publick-Commencement at Cambridge July V, MDCXCVI.",
            "url": "https://catalog.hathitrust.org/Record/008682174?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&filter%5B%5D=format%3ABook&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". of ATHEISM. 239\nwhen they fay, Nothing from Nothing;\nthey muſt ſo underſtand it, as excluding\nall Cauſes, both material and efficient.\nIn which fenſe it is moſt evidently and\ninfallibly true: being equivalent to this\npropoſition; that Nothing can make it\nJelf, or, Nothing cannot bring its no-\nfelf out of non-entity into Something",
            "filepath": "hat_texts/hat11169Eight.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.0038,
            "title": "Eight sermons preach'd at the Honourable Robert Boyle's lecture, in the first year, MDCXCII. 5th ed., to which is now added a sermon preach'd at the Publick-Commencement at Cambridge July V, MDCXCVI.",
            "url": "https://catalog.hathitrust.org/Record/008682174?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&filter%5B%5D=format%3ABook&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&ft=ft"
         }
      ],
      "quote_id": 111008,
      "title": "Serm."
   },
   {
      "author": "South.",
      "content": "There was no such thing as rendering evil for evil, when evil was truly a nonentity, and no where to be found.",
      "edition": "both",
      "headword": "NONENTITY",
      "matches": [
         {
            "author": "South, Robert, 1634-1716.",
            "best_match": false,
            "content": ".\nlice, or the Violences of Revenge: No ren-\ndring Evil for Evil, when Evil was truly a\nNon-entity,\nin God's Image.\nNone-ntity, and no where to be found",
            "filepath": "hat_texts/hat2183Twelv.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 71.2329,
            "title": "Twelve sermons ...",
            "url": "https://catalog.hathitrust.org/Record/008975272?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "South, Robert, 1634-1716.",
            "best_match": false,
            "content": ": No ren-\ndring Evil for Evil, when Evil was truly a\nNon-entity,\nin God's Image.\nNone-ntity, and no where to be found. An-\nger then was like the Sword of Juſtice, keen,\nbut innocent and righteous",
            "filepath": "hat_texts/hat2183Twelv.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 56.621,
            "title": "Twelve sermons ...",
            "url": "https://catalog.hathitrust.org/Record/008975272?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "South, Robert, 1634-1716.",
            "best_match": false,
            "content": ". For there have been\nſuch, as have aſſerted, \"That there is no ſuch\nthing in the World as Motion : That Con-\ntradiétions may be true. There has not been\nwanting one, that has denied Snow to be\nwhite",
            "filepath": "hat_texts/hat2183Twelv.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 54.1284,
            "title": "Twelve sermons ...",
            "url": "https://catalog.hathitrust.org/Record/008975272?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Mrs. E. D. E. N. Southworth",
            "best_match": false,
            "content": "! Well, I have hearn of such things happening to other\n    folks, and why not to me and poor Hannah? Why, sir, I would be\n    the happiest man in the world, if I thought as how I had all\n    them there years to live long o' Hannah and the little uns in\n    this pleasant world",
            "filepath": "gut_texts/gut30153Ishma.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 53.9535,
            "title": "Ishmael",
            "url": "https://www.gutenberg.org/files/15774/15774-h/15774-h.htm"
         },
         {
            "author": "Mrs. E. D. E. N. Southworth",
            "best_match": false,
            "content": ".\n        Tupper.\n\nIn this persevering labor Ishmael cheerfully passed the\n    winter months.\nHe had not heard one word of Claudia, or of her father,\n    except such scant news as reached him through the judge's\n    occasional letters to the overseer",
            "filepath": "gut_texts/gut30153Ishma.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 53.7037,
            "title": "Ishmael",
            "url": "https://www.gutenberg.org/files/15774/15774-h/15774-h.htm"
         }
      ],
      "quote_id": 3052,
      "title": ""
   },
   {
      "author": "Arbut. and Pope\u2019s",
      "content": "We have heard, and think it pity that your inquisitive genius should not be better employed, than in looking after that theological nonentity.",
      "edition": "both",
      "headword": "NONENTITY",
      "matches": [],
      "quote_id": 82196,
      "title": "Mart. Scrib."
   },
   {
      "author": "Bentley.",
      "content": "When they say nothing from nothing, they must understand it as excluding all causes. In which sense it is most evidently true; being equivalent to this proposition, that nothing can make itself, or, nothing cannot bring its no-self out of nonentity into something.",
      "edition": "both",
      "headword": "NONENTITY",
      "matches": [
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". For\nwhen they fay, Nothing from Nothing5 they must\nso understand it, as excluding all Causes, both ma-\nterial and efficient. In which fense it is most evi-\ndently and infallibly true: being equivalent to this\nproposition 5 that Nothing can make it self, or,\nNothing cannot bring its no self out of non-entity\ninto Something",
            "filepath": "hat_texts/hat977The-f.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 78.4762,
            "title": "The folly and unreasonableness of atheism demonstrated from the advantage and pleasure of a religious life, the faculties of humane souls, the structure of animate bodies, & the...",
            "url": "https://catalog.hathitrust.org/Record/001925709?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". For when they ſay,\nNothing from Nothing ; they muſt ſo underſtand it, as\nexcluding all Cauſes, both material and efficient. In\nwhich ſenſe it is moſt evidently and infallibly true: be-\ning equivalent to this propoſition; that nothing can\nmake it ſelf, or, Nothing cannot bring its no-ſelf out of\nnon-entity into Something",
            "filepath": "hat_texts/hat5601The-f.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 77.0398,
            "title": "The folly and unreasonableness of atheism : demonstrated from the advantage and pleasure of a religious life, the faculties of human souls, the structure of animate bodies, &...",
            "url": "https://catalog.hathitrust.org/Record/100170743?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". For when they ſay, Nothing from No-\nthing ; they muſt ſo underſtand it, as excluding all\nCauſes, both material and efficient. In which\nfence it is moſt evidently and infallibly true: be.\ning equivalent to this propoſition; that nothing can\nmake it ſelf, or, Nothing cannot bring its no-ſelf\nout of non enticy into Something",
            "filepath": "hat_texts/hat1027The-f.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.3833,
            "title": "The folly and unreasonableness of atheism ... in eight sermons preached at the lecture founded by the Honourable Robert Boyle, esquire; in the first year MDCXCII.",
            "url": "https://catalog.hathitrust.org/Record/001925703?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". of ATHEISM. 239\nwhen they fay, Nothing from Nothing;\nthey muſt ſo underſtand it, as excluding\nall Cauſes, both material and efficient.\nIn which fenſe it is moſt evidently and\ninfallibly true: being equivalent to this\npropoſition; that Nothing can make it\nJelf, or, Nothing cannot bring its no-\nfelf out of non-entity into Something",
            "filepath": "hat_texts/hat10912Eight.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.0038,
            "title": "Eight sermons preach'd at the Honourable Robert Boyle's lecture, in the first year, MDCXCII. 5th ed., to which is now added a sermon preach'd at the Publick-Commencement at Cambridge July V, MDCXCVI.",
            "url": "https://catalog.hathitrust.org/Record/008682174?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&filter%5B%5D=format%3ABook&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&ft=ft"
         },
         {
            "author": "Bentley, Richard, 1662-1742.",
            "best_match": false,
            "content": ". of ATHEISM. 239\nwhen they fay, Nothing from Nothing;\nthey muſt ſo underſtand it, as excluding\nall Cauſes, both material and efficient.\nIn which fenſe it is moſt evidently and\ninfallibly true: being equivalent to this\npropoſition; that Nothing can make it\nJelf, or, Nothing cannot bring its no-\nfelf out of non-entity into Something",
            "filepath": "hat_texts/hat11169Eight.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 74.0038,
            "title": "Eight sermons preach'd at the Honourable Robert Boyle's lecture, in the first year, MDCXCII. 5th ed., to which is now added a sermon preach'd at the Publick-Commencement at Cambridge July V, MDCXCVI.",
            "url": "https://catalog.hathitrust.org/Record/008682174?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&filter%5B%5D=format%3ABook&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&ft=ft"
         }
      ],
      "quote_id": 111008,
      "title": ""
   },
   {
      "author": "South.",
      "content": "There was no such thing as rendering evil for evil, when evil was truly a nonentity, and no where to be found.",
      "edition": "both",
      "headword": "NONENTITY",
      "matches": [
         {
            "author": "South, Robert, 1634-1716.",
            "best_match": false,
            "content": ".\nlice, or the Violences of Revenge: No ren-\ndring Evil for Evil, when Evil was truly a\nNon-entity,\nin God's Image.\nNone-ntity, and no where to be found",
            "filepath": "hat_texts/hat2183Twelv.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 71.2329,
            "title": "Twelve sermons ...",
            "url": "https://catalog.hathitrust.org/Record/008975272?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "South, Robert, 1634-1716.",
            "best_match": false,
            "content": ": No ren-\ndring Evil for Evil, when Evil was truly a\nNon-entity,\nin God's Image.\nNone-ntity, and no where to be found. An-\nger then was like the Sword of Juſtice, keen,\nbut innocent and righteous",
            "filepath": "hat_texts/hat2183Twelv.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 56.621,
            "title": "Twelve sermons ...",
            "url": "https://catalog.hathitrust.org/Record/008975272?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "South, Robert, 1634-1716.",
            "best_match": false,
            "content": ". For there have been\nſuch, as have aſſerted, \"That there is no ſuch\nthing in the World as Motion : That Con-\ntradiétions may be true. There has not been\nwanting one, that has denied Snow to be\nwhite",
            "filepath": "hat_texts/hat2183Twelv.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 54.1284,
            "title": "Twelve sermons ...",
            "url": "https://catalog.hathitrust.org/Record/008975272?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft"
         },
         {
            "author": "Mrs. E. D. E. N. Southworth",
            "best_match": false,
            "content": "! Well, I have hearn of such things happening to other\n    folks, and why not to me and poor Hannah? Why, sir, I would be\n    the happiest man in the world, if I thought as how I had all\n    them there years to live long o' Hannah and the little uns in\n    this pleasant world",
            "filepath": "gut_texts/gut30153Ishma.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 53.9535,
            "title": "Ishmael",
            "url": "https://www.gutenberg.org/files/15774/15774-h/15774-h.htm"
         },
         {
            "author": "Mrs. E. D. E. N. Southworth",
            "best_match": false,
            "content": ".\n        Tupper.\n\nIn this persevering labor Ishmael cheerfully passed the\n    winter months.\nHe had not heard one word of Claudia, or of her father,\n    except such scant news as reached him through the judge's\n    occasional letters to the overseer",
            "filepath": "gut_texts/gut30153Ishma.txt",
            "lccn": "-1",
            "rank": 0,
            "score": 53.7037,
            "title": "Ishmael",
            "url": "https://www.gutenberg.org/files/15774/15774-h/15774-h.htm"
         }
      ],
      "quote_id": 3052,
      "title": ""
   },
   {
      "author": "Arbuthnot and Pope.",
      "content": "We have heard, and think it pity that your inquisitive genius should not be better employed, than in looking after that theological nonentity.",
      "edition": "both",
      "headword": "NONENTITY",
      "matches": [],
      "quote_id": 82196,
      "title": ""
   },
   {
      "author": "Brown\u2019s",
      "content": "A method of many writers, which depreciates the esteem of miracles is, to salve not only real verities, but also non-existences.",
      "edition": "1",
      "headword": "NONEXISTENCE",
      "matches": [],
      "quote_id": 124520,
      "title": "Vulgar Errours,"
   },
   {
      "author": "Brown\u2019s",
      "content": "A method of many writers, which depreciates the esteem of miracles is, to salve not only real verities, but also nonexistences.",
      "edition": "4",
      "headword": "NONEXISTENCE",
      "matches": [],
      "quote_id": 44040,
      "title": "Vulgar Errours."
   }
];

function loadedHandler() {
  var searchParameters;
  (window.onpopstate = function () {
      var match,
          pl     = /\+/g,  // Regex for replacing addition symbol with a space
          search = /([^&=]+)=?([^&]*)/g,
          decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
          query  = window.location.search.substring(1);

      searchParameters = {};
      while (match = search.exec(query))
         searchParameters[decode(match[1])] = decode(match[2]);
  })();
  $.ajax({
    type: "GET",
    url: "php/" + searchParameters["chosenSearchOption"] + ".php",
    dataType: "json",
    contentType: "application/json",
    //data: JSON.stringify(searchParameters),
    success: function(data) {
      console.log(data);
      $("#testtable2").html(json2Table2(data));
    },
    error: function(data) {
      console.log("error.");
      console.log(data);
    }
  });
}

$("#testtable2").ready(loadedHandler);


//output = document.getElementById('testtable');
//output.innerHTML = json2Table(data);
output2 = document.getElementById('testtable2');
//output2.innerHTML = json2Table2(data3);
let resultsTable = document.getElementById('testtable2');
//$("#testtable2").ready(loadedHandler);
