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

if($("#searchRandCol").is(":visible")) {

}

function updateSearchOption(searchOption) {
  $("#chosenSearchOption").attr("value", searchOption);
    switch(searchOption) {
      case ('get_matches_by_headword'):
        $("#chosenSearch").html("Matches by Headword");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchText").prop("disabled", false);
        }
        break;
      case ("get_matches_by_author"):
        $("#chosenSearch").html("Matches by Author");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchText").prop("disabled", false);
        }
        break;
      case ("get_matches_by_title"):
        $("#chosenSearch").html("Matches by Title");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchText").prop("disabled", false);
        }
        break;
      case ("get_matches_by_random"):
        $("#chosenSearch").html("Random Selection");
        if($("#searchTextCol").is(":visible")) {
          $("#searchText").prop("disabled", true);
          $("#searchRandomDropdown").prop("disabled", false);
        }
        break;
    }
}

function testSubmit() {
  var serialData = window.location.search.substring(1);
  $.post("php/get_matches_by_title.php",
    serialData,
    function(data) {
      console.log(data);
    });

}

function loadedHandler() {
  // Decodes the search paramaters from the url with a regex and stores in searchParameters array.
  // Access the array with searchParameters["<formNameValue>"].
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
  console.log(window.location.search.substring(1));

  // This data variable is the JSON sent to the API. Once instantiated, the data is filled based on the
  // search type parsed from the results page URL.
  var data = {};
  switch (searchParameters["chosenSearchOption"]) {
    case ('get_matches_by_headword'):
      data.headword = searchParameters["searchBox"];
      //data.corpus = searchParameters["searchCorpus"];
      break;
    case ("get_matches_by_author"):
      data.author = searchParameters["searchBox"];
      //data.corpus = searchParameters["searchCorpus"];
      break;
    case ("get_matches_by_title"):
      data.title = searchParameters["searchBox"];
      //data.corpus = searchParameters["searchCorpus"];
      break;
    case ("get_matches_by_random"):
      data.number = searchParameters["number"];
      //data.corpus = searchParameters["searchCorpus"];
      break;
  }

  var serialData = window.location.search.substring(1);
  var url = "php/" + searchParameters["chosenSearchOption"] + ".php";
  $.post(url,
    serialData,
    function(data) {
      console.log(data);
      $("#testtable2").html(json2Table2(JSON.parse(data)));
    });

/*
  $.ajax({
    type: "POST",
    url: "php/" + searchParameters["chosenSearchOption"] + ".php",
    dataType: "json",
    //contentType: "application/json",
    data: data,
    success: function(data) {
      console.log(data);
      $("#testtable2").html(json2Table2(JSON.parse(data)));
    },
    error: function(data, responseText) {
      console.log("error.");
      console.log(data);
      console.log(responseText);
    }
  });
  */
}

$("#testtable2").ready(loadedHandler);

output2 = document.getElementById('testtable2');
//output2.innerHTML = json2Table2(data3);
let resultsTable = document.getElementById('testtable2');
