"use strict"
const answerSuggestion = document.querySelector('.writing_good_answers');
const closeSuggestionBox = document.querySelector('.close-suggestion')
const sample = document.querySelector('.sample');

const AnswerBox = document.getElementById("id_comment");

closeSuggestionBox.addEventListener("click", function () {
  console.log("Hi");
  answerSuggestion.classList.add("hidden");
});
