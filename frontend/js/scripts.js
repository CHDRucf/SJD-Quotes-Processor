function login() {
  let loginUrl = "php/login.php";
  let loginForm = $("#loginForm");
  let loginInfo = loginForm.serialize();
  //alert(loginInfo);
  $.ajax({
    type: "POST",
    contentType: "application/x-www-form-urlencoded; charset=UTF-8",
    url: loginUrl,
    dataType: "json",
    data: loginInfo,
    success: function(json) {
      let responseData = JSON.parse(JSON.stringify(json));
      if (responseData.message == "success") {
        alert("success! Logging in...");
        window.location = "home.html";
      }
      else if (responseData.message == "username or password is invalid"){
        alert("Error: Username or Password is invalid.");
        window.location = "login.html";
      }
    },
    error: function(response, data) {
      console.log(data);
      console.log(response);
      alert("Error: Something went wrong.");
      window.location = "login.html";
    }
  })
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
  alert("JSON keys found: " + Object.keys(json).length);
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
      return `<tr id="quoteRow">${tds}</tr>`;
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

//  if (Object.keys(data.matches).length > 0) {
    matches = createMatchTable(data.matches, data.quote_id);
  return `
    <td id="headwordCol" scope="row">${data.headword}</td>
    <td id="quoteCol">${data.content}</td>
    <td id="quoteTitleCol">${data.title}</td>
    <td id="quoteAuthorCol">${data.author}</td>
    <td id="editionCol">${data.edition}</td>
    ${matches}
  `
  //<td id="quoteIDCol">${data.quote_id}</td>
}

function createMatchTable(matchArr, quoteID) {
  let headerRow = createMatchHeaderRowCols();
  // Check if the quote has any matches. If not, use an empty matches table.
  if (matchArr.length == 0) {
    headerRow = `<th style="width:100%" id="emptyHeader">No Matches</th>`
    return `
      <tr id="matchRow">
        <td id="matchTableDatum">
          <table id="matchTable" class="table table-bordered">
            <thead>
            <tr>
              ${headerRow}
            </tr>
            </thead>
              <td id="noMatchesFoundDatum">No matches found. Either this quote has no matches, or matches may have been filtered by search options.</td>
          </table>
        </td>
      </tr>
      `
  }
  let cols = Object.keys(matchArr[0]);

  let rows = matchArr
    .map(row => {
      //let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
      let tds = createMatchRowCols(row, cols, quoteID);
      return `<tr>${tds}</tr>`;
    })
    .join("");

  // Note: no tbody tags needed; Boostrap generates tbody tags around tr tags.
  return `
    <tr id="matchRow">
      <td id="matchTableDatum">
        <table id="matchTable" class="table table-bordered">
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

function createMatchRowCols(row, cols, quoteID) {
  let data = JSON.parse(JSON.stringify(row));
  var markedBest = "";
  if (data.flag) {
    markedBest = "checked";
  }
  // Store quote ID in Best Match column. This value will be used to evaluate all matches for that quote
  // ID to make sure only one best match is selected at a time.
  return `
    <td id="ratingCol" scope="row">${data.score}</td>
    <td id="matchQuoteCol">${data.content}</td>
    <td id="matchTitleCol">${data.title}</td>
    <td id="matchAuthorCol">${data.author}</td>
    <td id="flagCol" data-matchID="${data.match_id}" data-work_metadataID="${data.work_metadata_id}"><input type="radio" id="bestFlag" name="${quoteID}" ${markedBest}></td>
    <td id="urlCol">${data.url}</td>
  `
  //<td id="matchIDCol">${data.matchID}</td>
}

function updateSearchOption(searchOption) {
  $("#chosenSearchOption").attr("value", searchOption);
    switch(searchOption) {
      case ('get_matches_by_headword'):
        $("#chosenSearch").html("Matches by Headword");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchRandRow").prop("hidden", true);
          $("#searchText").prop("disabled", false);
          $("#textFormatDropdown").prop("disabled", false);
          $("#searchTextRow").prop("hidden", false);
        }
        break;
      case ("get_matches_by_author"):
        $("#chosenSearch").html("Matches by Author");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchRandRow").prop("hidden", true);
          $("#searchText").prop("disabled", false);
          $("#textFormatDropdown").prop("disabled", false);
          $("#searchTextRow").prop("hidden", false);
        }
        break;
      case ("get_matches_by_title"):
        $("#chosenSearch").html("Matches by Title");
        if($("#searchRandCol").is(":visible")) {
          $("#searchRandomDropdown").prop("disabled", true);
          $("#searchRandRow").prop("hidden", true);
          $("#searchText").prop("disabled", false);
          $("#textFormatDropdown").prop("disabled", false);
          $("#searchTextRow").prop("hidden", false);
        }
        break;
      case ("get_matches_by_random"):
        $("#chosenSearch").html("Random Selection");
        if($("#searchTextCol").is(":visible")) {
          $("#searchText").prop("disabled", true);
          $("#textFormatDropdown").prop("disabled", true)
          $("#searchTextRow").prop("hidden", true);
          $("#searchRandomDropdown").prop("disabled", false);
          $("#searchRandRow").prop("hidden", false);
        }
        break;
    }
}

function floatingBarLoadHandler() {
  var params;
  (window.onpopstate = function () {
      var match,
          pl     = /\+/g,  // Regex for replacing addition symbol with a space
          search = /([^&=]+)=?([^&]*)/g,
          decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
          query  = window.location.search.substring(1);

      params = {};
      while (match = search.exec(query))
         params[decode(match[1])] = decode(match[2]);
  })();

  // Prevent HTML injection
  var searchTerm = "" + params["searchBox"];

  switch (params["chosenSearchOption"]) {
    case ('get_matches_by_headword'):
      $("#searchTypeHeader").html("Matches by Headword: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html("\"" + searchTerm + "\"");
      break;
    case ("get_matches_by_author"):
      $("#searchTypeHeader").html("Matches by Author: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html("\"" + searchTerm + "\"");
      break;
    case ("get_matches_by_title"):
      $("#searchTypeHeader").html("Matches by Title: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html("\"" + searchTerm + "\"");
      break;
    case ("get_matches_by_random"):
      $("#searchTypeHeader").html("Random Selection: <span id=\"searchTermSpan\"></span>");
      $("#searchTermSpan").html(params["number"] + " quotes");
      break;
  }

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
  //console.log(window.location.search.substring(1));

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

/*
  $.getJSON("test.json", function(json) {
    $("#testtable2").html(json2Table2(json));
  });
*/

  var serialData = window.location.search.substring(1);
  var table;
  var url = "php/" + searchParameters["chosenSearchOption"] + ".php";
  if (window.location.href.includes("results.html")){
    $("#dataTablesEx, #mask").addClass("loading");

    $.ajax({
      type: "POST",
      contentType: "application/x-www-form-urlencoded; charset=UTF-8",
      url: url,
      dataType: "json",
      data: serialData,
      success: function(json) {
        console.log(json);
        $("#dataTablesEx, #mask").removeClass("loading");

        table = $("#dataTablesEx").DataTable({
        "data": json,
        "dataSrc": "",
          "columns": [
            {"data": "headword",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "headwordCol");
                $(td).attr("scope", "row");
                $(td).closest("tr").attr("id", "quoteRow");
                $(td).closest("tr").attr("data-quoteID", rowData.quote_id);
            }},
            {"data": "content",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "quoteCol");
            }},
            {"data": "title",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "quoteTitleCol");
            }},
            {"data": "author",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "quoteAuthorCol");
            }},
            {"data": "edition",
            "createdCell": function(td, cellData, rowData, row, col) {
                $(td).attr("id", "editionCol");
                if (cellData == "both") {
                  $(td).html("1/4");
                }
            }}
          ],
          "deferRender": true,
          "fixedHeader": true,
          "fixedFooter": true

        });
      },
      error: function(data){
        $("#mask").removeClass("loading");
        console.log("error retrieving data.");
        console.log(data);
      }

    });
  }

  // Match subtable handler
  /*$("#dataTablesEx").on("click", "tbody tr td", function() {
    var tr = $(this).closest("tr");
    var row = table.row(tr);

    if (tr.attr("id") == "quoteRow") {
      if (row.child.isShown()){
        row.child.hide();
        tr.removeClass("shown");
      }
      else {
        row.child(createMatchTable2(row.data())).show();
        tr.addClass("shown");
      }
    }
  });*/

  // Dynamic match subtable handler
  $("#dataTablesEx").on("click", "tbody tr td", function() {
    var tr = $(this).closest("tr");
    var row = table.row(tr);

    if (tr.attr("id") == "quoteRow") {
      if (row.child.isShown()){
        row.child.hide();
        tr.removeClass("shown");
      }
      else {
        var serialData = "quote_id=" + row.data().quote_id;
        console.log(serialData);

        $.ajax({
          type: "POST",
          contentType: "application/x-www-form-urlencoded; charset=UTF-8",
          url: "php/get_quote_matches.php",
          dataType: "json",
          data: serialData,
          success: function(responseData) {
            row.child(createMatchTable2(responseData)).show();
            tr.addClass("shown");
          },
          error: function(data) {
            console.log(data);
            alert("Something went wrong when retrieving match data.");
          }
        });
        row.child(createMatchTable2(row.data())).show();
        tr.addClass("shown");
      }
    }
  })

  // Best Match handlers
  $("body").on("mousedown", "#flagCol input[type='radio']", function() {

    var wasChecked = $(this).prop("checked");
    this.turnOff = wasChecked;
    //$(this).prop('checked', !wasChecked);

  });

  $("body").on("click", "#flagCol input[type='radio']", function(){
    clickedInput = $(this);
    var matchID = clickedInput.closest("td").attr("data-matchID");
    var work_metadataID = clickedInput.closest("td").attr("data-work_metadataID");
    var quoteID = clickedInput.attr("name");
    var serialData = "quote_id=" + quoteID +  "&match_id=" + matchID + "&work_metadata_id=" + work_metadataID;
    console.log(serialData);

    // This button was checked: add its match to the best_matches table
    if (!this.turnOff)
    {
      var url = "php/set_best_match.php";
      $.ajax({
        type: "POST",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: url,
        data: serialData,
        success: function(data) {
          console.log(data);
          alert("Best match added.");
          clickedInput.prop("checked", !this.turnOff);
          this["turning-off"] = !this.turnOff;
        },
        error: function(data) {
          console.log(data);
          alert("Error. Best match not added.");
        }
      });
    }
    // This button was unchecked: add its match to the best_matches table
    else {
      var url = "php/unset_best_match.php";
      $.ajax({
        type: "POST",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        url: url,
        data: serialData,
        success: function() {
          alert("Best match removed.");
          clickedInput.prop("checked", false);
          this["turning-off"] = !this.turnOff;
        },
        error: function() {
          alert("Error. Best match not removed.");
        }
      });
    }
  });
}

function createMatchTable2(rowData) {
  let matchArr = rowData.matches;
  let quoteID = rowData.quote_id;
  let headerRow = createMatchHeaderRowCols();
  // Check if the quote has any matches. If not, use an empty matches table.
  if (matchArr.length == 0) {
    headerRow = `<th style="width:100%" id="emptyHeader" colspan="5">No Matches</th>`
    return `
      <table id="matchTable" class="table table-bordered">
        <thead>
          <tr>
            ${headerRow}
          </tr>
        </thead>
          <td id="noMatchesFoundDatum" colspan="5">No matches found. Either this quote has no matches, or matches may have been filtered by search options.</td>
      </table>
      `
  }
  let cols = Object.keys(matchArr[0]);

  let rows = matchArr
    .map(row => {
      //let tds = cols.map(col => `<td>${row[col]}</td>`).join("");
      let tds = createMatchRowCols(row, cols, quoteID);
      return `<tr>
                ${tds}
              </tr>`;
    })
    .join("");

  // Note: no tbody tags needed; Boostrap generates tbody tags around tr tags.
  return `
    <table id="matchTable" class="table table-bordered">
      <thead>
        <tr>
          ${headerRow}
        </tr>
      </thead>
        ${rows}
    </table>
  `
}

$(document).ready(loadedHandler);
$("#floatingBar").ready(floatingBarLoadHandler);
/*
$("body").on("click", "#quoteRow td, #quoteRow th", function() {
  $(this).closest("tr").next("tr").children().toggle();
});*/
$("#returnToSearch").on("click", function() {
  window.location = "home.html";
});

output2 = document.getElementById('testtable2');
//output2.innerHTML = json2Table2(data3);
let resultsTable = document.getElementById('testtable2');
