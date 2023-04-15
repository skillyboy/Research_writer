$('.ui.dropdown').dropdown({
    forceSelection: false
});






const chapterForm = document.getElementById('chapter-form');
const chaptersDataBox = document.getElementById('chapters-data-box');
const chapterDropdown = document.getElementById('chapters');

const topicsText = document.getElementById('topics-text');
const topicsDropdown = document.getElementById('topics');
const topicsDataBox = document.getElementById('topics-data-box');


const csrf = document.getElementsByName('csrfmiddlewaretoken');

// Load initial data for the chapters dropdown
$.ajax({
  type: 'GET',
  url: '/chapters-json/',
  success: function(response){
    console.log(response.data);
    const chaptersData = response.data;
    chaptersData.map(item => {
      const option = document.createElement('div');
      option.textContent = item.name;
      option.setAttribute('class', 'item');
      option.setAttribute('data-value', item.name);
      chaptersDataBox.appendChild(option);
    });
  },
  error: function(error){
    console.log(error);
  }
});

// When the user selects a chapter, load the corresponding topics
chapterDropdown.addEventListener('change', e => {
  console.log(e.target.value);
  const selectedChapter = e.target.value;
  topicsText.textContent = "Loading...";
  topicsDataBox.innerHTML = "";
//   topicsText.classList.add("default")
  
  $.ajax({
    type: 'GET',
    url: `topics-json/${selectedChapter}/`,
    success: function(response){
      console.log(response.data);
      const topicsData = response.data;
      topicsData.map(item => {
        const option = document.createElement('div');
        option.textContent = item.name;
        option.setAttribute('class', 'item');
        option.setAttribute('data-value', item.name);
        topicsDataBox.appendChild(option);
      });
      
      topicsText.textContent = "Choose a topic";
    },
    error: function(error){
      console.log(error);
    }
  });
});

// ===================================================


// Create or update Topics

const savechapbtn = document.querySelector('.savechapbtn');
const topicform = document.querySelector('.topicform');
topicform.addEventListener('submit', (e)=>{
  e.preventDefault()
  const newform = new FormData()
  newform.append('content', document.querySelector('.content').value)
  newform.append('topicid', document.querySelector('.topicid').value)
  newform.append('csrfmiddlewaretoken', '{{csrf_token}}')
  axios.post('/savetopicform/', newform)
  .then((resp)=>{
    if(resp.data.status ==='success'){
      savechapbtn.click()
      topicform.reset()
    }
  })
  .catch((err)=>{
    console.log(err)
  })
})