let todoList = [
  {
    item: 'Buy Milk',
    duedate: '10/4/2003'
},
{
  item: 'Go to college',
  duedate: '13/5/2005'
}
];


displayItems();

function addTodo(){
  let inputElement = document.querySelector('#todo-input');
  let dateElement = document.querySelector('#todo-date');


  let todoItem = inputElement.value;
  let tododate = dateElement.value;

  todoList.push({item: todoItem, duedate: tododate});
  inputElement.value = '';
  dateElement.value = '';
  displayItems();

}

function displayItems(){
  let containerElement = document.querySelector
  ('.todo-container');
  let newHtml =''; 
  for(let i = 0; i < todoList.length; i++) {
    
    let {item, duedate} = todoList[i];
    newHtml += `
    
    <span>${item}</span>
    <span>${duedate}</span>
    <button class="btn-delete" onclick="todoList.splice(${i}, 1);
    displayItems(); ">Delete</button>
    
    `;
  }
  containerElement.innerHTML = newHtml;
}