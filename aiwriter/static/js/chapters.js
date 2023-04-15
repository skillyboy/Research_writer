
// // Get the elements
// const renameBtns = document.querySelectorAll('.rename-icon');
// const inputContainers = document.querySelectorAll('.input-container');
// const renameForm = document.querySelector('#rename-form');
// const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
// const addindexbtn = document.querySelector('#addindexbtn');
// const form = document.querySelector('#addtopicform');




// // ===========================GET THE CHAPTER TO VIEW=================
// $(document).ready(function() {
//     // Function to fetch and display the topics for a given chapter
//     function getTopicsForChapter(chapterId) {
//       $.ajax({
//         url: '/get-topics/',
//         method: 'GET',
//         data: {'chapter_id': chapterId},
//         success: function(response) {
//           // Clear the previous topics and append the new ones to the container
//           $('#topics-container').empty().append(response.html);
//         },
//         error: function(response) {
//           alert(response.responseJSON.error);
//         }
//       });
//     }
  
//     // Add an event listener to the dropdown to fetch and display the topics for the selected chapter
//     $('#chapter_select').on('change', function() {
//       var chapterId = $(this).val();
//       getTopicsForChapter(chapterId);
//     });
  
//     // Initialize the topics for the currently selected chapter
//     var selectedChapterId = $('#chapter_select').val();
//     getTopicsForChapter(selectedChapterId);
//   });

  
// // ====================TOGGLE RENAME VISIBITY========================
// // Add click event listeners to toggle the visibility of the input containers
// renameBtns.forEach((renameBtn, index) => {
//     renameBtn.addEventListener('click', () => {
//     // Toggle the "input-container" visibility
//     inputContainers[index].style.display = inputContainers[index].style.display === 'none' ? 'block' : 'none';
//     });
// });



// // ===================RENAME A TOPIC FORM=========================
// // Add submit event listener to rename form
// renameForm.addEventListener('submit', (e) => {
//     e.preventDefault();

//     const renameBtn = e.submitter;
//     const topicId = renameBtn.dataset.topicId;
//     const inputContainer = renameBtn.closest('.input-container');
//     const renameInput = inputContainer.querySelector('.rename-input');
//     const newName = renameInput.value;

//     // Make AJAX request to update topic name
//     const renameUrl = `/rename_topic/${topicId}/`;
//     const formData = new FormData();
//     formData.append('new_name', newName);
//     formData.append('csrfmiddlewaretoken', csrfToken);

//     axios.post(renameUrl, formData)
//     .then((response) => {
//         // Update topic name in the UI
//         const topicName = inputContainer.closest('.modal-body').querySelector('h5');
//         topicName.textContent = newName;

//         // Hide the rename input
//         inputContainer.style.display = 'none';
//     })
//     .catch((error) => {
//         console.error(error);
//     });
// });

// // =================== ADD A NEW TOPIC A CHAPTER==========================



// form.addEventListener('submit', (e)=>{
//   e.preventDefault()
//   const addindexform = new FormData()
//   addindexform.append('content', document.querySelector('#name').value)
//   addindexform.append('chapter_id', document.querySelector('#chapter_id').value)
//   addindexform.append('csrfmiddlewaretoken', '{{csrf_token}}')
//   axios.post('/add_newtopic_name/', addindexform)
//   .then((resp)=>{
//     if(resp.data.status ==='success'){
//       addindexbtn.click()
//       form.reset()
//     }
//   })
//   .catch((err)=>{
//     console.log(err)
//   })
// });

// // ==================================================================

// // =====================DELETE  GENERATED TOPIC FROM SAVED =====================       
// function deleteSubtopic(topicId) {
//   if (confirm('Are you sure you want to delete this subtopic?')) {
//     $.ajax({
//       type: 'POST',
//       url: '/del-subtopic/' + topicId + '/',
//       data: {
//         csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
//       },
//       success: function(response) {
//         if (response === 'ok') {
//           // Remove the deleted subtopic from the DOM
//           $('#subtopic-' + topicId).remove();
//         } else {
//           alert('An error occurred while deleting the subtopic');
//         }
//       },
//       error: function() {
//         alert('An error occurred while deleting the subtopic');
//       }
//     });
//   }
// }

// // ========================SAVE GENERATED TOPIC==================================

// function saveContent(topicId) {
//   var content = $('#content-' + topicId).val();
//   if (content.trim() === '') {
//     alert('Please enter some content');
//     return;
//   }
//   var chapterId = $('#chapter-id').val();
//   var indexId = $('#index-id').val();
//   $.ajax({
//     type: 'POST',
//     url: '/save-subtopic/',
//     data: {
//       chapter_id: chapterId,
//       index_id: indexId,
//       content: encodeURIComponent(content),
//       csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
//     },
//     success: function(response) {
//       if (response.message) {
//         alert('Content saved successfully');
//       } else {
//         alert('An error occurred while saving the content');
//       }
//     },
//     error: function() {
//       alert('An error occurred while saving the content');
//     }
//   });
// }

