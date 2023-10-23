if (window.location.pathname === '/register') {
  document.getElementById('registration-form').addEventListener('submit', handleRegister)
}

if (window.location.pathname === '/client-home') {
  document.getElementById('logout').addEventListener('click', handleLogout)
  generateMeetingTable()
}

const urlArr = window.location.href.split('/')
if (urlArr[urlArr.length - 2] === 'meeting') {
  const meetings = JSON.parse(localStorage.getItem('meetings'))
  const currentMeeting = meetings.filter(meeting => meeting.id === urlArr[urlArr.length - 1])[0]
  const attendArr = currentMeeting.attendees.split(', ')
  const ul = document.getElementById('attendees-list')

  attendArr.forEach(renderProductList)

  function renderProductList (element) {
    const li = document.createElement('li')
    li.setAttribute('class', 'item')

    ul.appendChild(li)

    li.innerHTML = element
  }
  document.getElementById('meeting-date').innerHTML = currentMeeting.meetingDate
  document.getElementById('meeting-name').innerHTML = currentMeeting.meetingName
  document.getElementById('meeting-room').innerHTML = currentMeeting.meetingRoom
  document.getElementById('meeting-time').innerHTML = currentMeeting.meetingTime
  document.getElementById('organizer').innerHTML = currentMeeting.organizer
  document.getElementById('room-type').innerHTML = currentMeeting.type
  // Currently reprints attendees as just one string. Not as list elements
  document.getElementById('attendees-list').innerHTML = currentMeeting.attendees
}
if (window.location.pathname === '/create-meeting') {
  document.getElementById('logout').addEventListener('click', handleLogout)
  document.getElementById('create-meeting-form').addEventListener('submit', handleCreateMeeting)
  document.addEventListener('DOMContentLoaded', populateAttendeesDropdown)
}

if (window.location.pathname === '/file-complaint') {
  document.getElementById('logout').addEventListener('click', handleLogout)
  document.getElementById('complaint-form').addEventListener('submit', handleFileComplaint)
  generateComplaintTable()
}

if (window.location.pathname === '/view-complaints') {
  document.getElementById('respond-to-complaint-form').addEventListener('submit', handleRespondToComplaint)
  generateComplaintsTable()
}

if (window.location.pathname === '/admin-view-meetings') {
  document.getElementById('room').onchange = handleRoomSwitcherChange
  document.getElementById('day-or-week').onchange = handleDayOrWeek

  addRoomsToSwitcher()
  generateMeetingTableDayView()
  generateMeetingTableWeekView()
}

if (window.location.pathname === '/') {
  document.getElementById('login-form').addEventListener('submit', handleLogin)
}

if (window.location.pathname === '/client-profile') {
  generatePaymentInformationTableHeaders()
  generatePaymentInformationTable()
  document.getElementById('logout').addEventListener('click', handleLogout)
  const userData = JSON.parse(localStorage.getItem('userData'))
  document.getElementById('firstName').innerHTML = userData.firstName
  document.getElementById('lastName').innerHTML = userData.lastName
  document.getElementById('first').value = userData.firstName
  document.getElementById('last').value = userData.lastName

  document.getElementById('edit-profile-form').addEventListener('submit', handleEditProfile)

  document.getElementById('edit-payment-btn').onclick = function () {
    const form = document.getElementById('edit-payment-form')
    const achForm = document.getElementById('ach-details')
    if (form.style.display === 'block') {
      form.style.display = 'none'
      achForm.style.display = 'none'
    } else {
      form.style.display = 'block'
      achForm.style.display = 'block'
    }
  }
  document.getElementById('payment-method').onchange = function () {
    const achForm = document.getElementById('ach-details')
    const ccForm = document.getElementById('credit-card-details')
    if (document.getElementById('payment-method').value === 'ach') {
      achForm.style.display = 'block'
      ccForm.style.display = 'none'
    } else {
      achForm.style.display = 'none'
      ccForm.style.display = 'block'
    }
  }

  document.getElementById('edit-profile-btn').onclick = function () {
    const form = document.getElementById('edit-profile-form')
    if (form.style.display === 'block') {
      form.style.display = 'none'
    } else {
      form.style.display = 'block'
    }
  }

  document.getElementById('edit-payment-form').addEventListener('submit', async function (event) {
    event.preventDefault()
    const paymentMethod = document.getElementById('payment-method').value
    if (paymentMethod === 'ach') {
      await fetch('/payment-information', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          paymentMethod,
          routingNumber: document.getElementById('routing-number').value,
          accountNumber: document.getElementById('account-number').value,
          accountName: document.getElementById('full-name-ach').value
        })
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            localStorage.setItem('userData', JSON.stringify(data.userData))
            window.location.href = '/client-profile'
          })
        }
      })
    } else {
      await fetch('/payment-information', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          paymentMethod,
          cardNumber: document.getElementById('card-number').value,
          accountName: document.getElementById('accountName').value,
          expirationDate: document.getElementById('expiration-date').value,
          securityCode: document.getElementById('security-code').value
        })
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            localStorage.setItem('userData', JSON.stringify(data.userData))
            window.location.href = '/client-profile'
          })
        }
      })
    }
  })
}

if (window.location.pathname === '/edit-rooms') {
  generateRoomTable()
  document.getElementById('room-form').addEventListener('submit', handleCreateRoom)
}

if (window.location.pathname === '/update-billing') {
  generateUpdateBillingTable()
}

async function handleLogin (event) {
  event.preventDefault()

  const username = document.getElementById('username').value
  const password = document.getElementById('password').value

  const encoder = new TextEncoder()
  const data = encoder.encode(password)
  const hash = await window.crypto.subtle.digest('SHA-256', data)
  const hashedPassword = Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('')

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username,
      password: hashedPassword
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
        window.location.href = data.redirectTo
      })
    } else if (response.status === 401) {
      document.getElementById('error-message').innerHTML = 'Invalid username or password'
    }
  })
}

async function handleCreateMeeting (event) {
  event.preventDefault()
  let type = document.getElementsByName('room-type')
  for (let i = 0; i < type.length; i++) {
    if (type[i].checked) {
      type = type[i].value
      break
    }
  }
  await fetch('/create-meeting', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      organizer: localStorage.getItem('username'),
      meetingName: document.getElementById('meeting-name').value,
      meetingDate: document.getElementById('date').value,
      meetingTime: document.getElementById('time').value,
      meetingRoom: document.getElementById('room').value,
      attendees: Array.from(document.getElementById('attendees-dropdown').options) // Convert HTMLCollection to Array
        .filter(option => option.selected) // Filter only the selected options
        .map(option => option.value),
      type
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
    } else if (response.status === 400) {
      response.json().then(data => {
        document.getElementById('error-message').innerHTML = data.message
      })
    }
  })
}
async function handleLogout (event) {
  event.preventDefault()

  fetch('/logout', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => {
    if (response.status === 200) {
      window.location.href = '/'
    }
  })
}

async function handleRegister (event) {
  event.preventDefault()

  const encoder = new TextEncoder()
  const data = encoder.encode(document.getElementById('password').value)
  const hash = await window.crypto.subtle.digest('SHA-256', data)
  const hashedPassword = Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('')

  const body = {
    firstName: document.getElementById('firstName').value,
    lastName: document.getElementById('lastName').value,
    username: document.getElementById('username').value,
    password: hashedPassword,
    type: 'client'
  }

  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  }).then(response => {
    if (response.status === 200) {
      window.location.href = '/client-home'
    } else if (response.status === 401) {
      document.getElementById('error-message').innerHTML = 'Username already exists'
    } else if (response.status === 400) {
      document.getElementById('error-message').innerHTML = 'Username must be a valid email address'
    }
  })
}

async function handleEditProfile (event) {
  event.preventDefault()
  const form = document.getElementById('edit-profile-form')
  await fetch('/edit-profile', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      firstName: form.elements[0].value,
      lastName: form.elements[1].value
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(body => {
        localStorage.setItem('userData', JSON.stringify(body.data))
        window.location.href = '/client-profile'
      })
    }
  })
}

function openModal () {
  const modal = document.getElementById('modify-attendees-modal')
  const attendeesList = document.getElementById('attendees-list')

  // Clear previous attendees
  attendeesList.innerHTML = ''

  // Populate the modal with attendees

  // Show the modal
  modal.style.display = 'block'

  // Close modal functionality
  document.getElementById('close-modal-btn').addEventListener('click', function () {
    modal.style.display = 'none'
  })
}

function populateAttendeesDropdown () {
  const attendeesDropdown = document.getElementById('attendees-dropdown')

  // Get user data from localStorage
  const userData = JSON.parse(localStorage.getItem('userData'))
  if (userData && userData.users) {
    const users = userData.users

    // Add an option for each user
    users.forEach(user => {
      const option = document.createElement('option')
      option.value = user // assuming each user has an email attribute
      option.textContent = user // show name if available, otherwise show email
      attendeesDropdown.appendChild(option)
    })
  }
}

function generateMeetingTable () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  const meetings = userData.meetings
  for (let i = 0; i < meetings.length; i++) {
    const meeting = meetings[i]
    const table = document.getElementById('meeting-table')
    const row = table.insertRow()
    const meetingName = row.insertCell(0)
    const meetingDate = row.insertCell(1)
    const meetingTime = row.insertCell(2)
    const meetingRoom = row.insertCell(3)
    const attendees = row.insertCell(4)
    const type = row.insertCell(5)
    const actions = row.insertCell(6)
    meetingName.innerHTML = meeting.meetingName
    meetingDate.innerHTML = meeting.meetingDate
    meetingTime.innerHTML = meeting.meetingTime
    meetingRoom.innerHTML = meeting.meetingRoom
    attendees.innerHTML = meeting.attendees
    type.innerHTML = meeting.type
    actions.innerHTML = '<button class="modify-attendees-btn">Modify Attendees</button>'
    actions.querySelector('.modify-attendees-btn').addEventListener('click', function () {
      openModal(meeting.attendees)
    })
  }
}

function generateComplaintTable () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  const complaints = userData.complaints
  for (let i = 0; i < complaints.length; i++) {
    const complaint = complaints[i]
    const table = document.getElementById('complaint-table')
    const row = table.insertRow()
    const subject = row.insertCell(0)
    const message = row.insertCell(1)
    const status = row.insertCell(2)
    const response = row.insertCell(3)
    subject.innerHTML = complaint.subject
    message.innerHTML = complaint.message
    status.innerHTML = complaint.status
    response.innerHTML = complaint.response ? complaint.response : ''
  }
}

function generatePaymentInformationTableHeaders () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  const paymentInformation = userData.paymentInformation
  const table = document.getElementById('payment-information-table')
  console.log(paymentInformation)
  if (paymentInformation === undefined) {
    const row = table.insertRow()
    const paymentMethod = row.insertCell(0)
    paymentMethod.innerHTML = 'No payment information on file'
  } else {
    if (paymentInformation.paymentMethod === 'credit-card') {
      const row = table.insertRow()
      const paymentMethod = row.insertCell(0)
      const accountName = row.insertCell(1)
      const cardNumber = row.insertCell(2)
      const expirationDate = row.insertCell(3)
      const securityCode = row.insertCell(4)
      paymentMethod.innerHTML = 'Payment Method'
      accountName.innerHTML = 'Card Name'
      cardNumber.innerHTML = 'Card Number'
      expirationDate.innerHTML = 'Expiration Date'
      securityCode.innerHTML = 'Security Code'
    } else {
      const row = table.insertRow()
      const paymentMethod = row.insertCell(0)
      const accountNumber = row.insertCell(1)
      const routingNumber = row.insertCell(2)
      const accountName = row.insertCell(3)
      paymentMethod.innerHTML = 'Payment Method'
      accountNumber.innerHTML = 'Account Number'
      routingNumber.innerHTML = 'Routing Number'
      accountName.innerHTML = 'Account Name'
    }
  }
}

function generatePaymentInformationTable () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  const paymentInformation = userData.paymentInformation
  const table = document.getElementById('payment-information-table')
  const row = table.insertRow()
  if (paymentInformation === undefined) { /* empty */ } else {
    if (paymentInformation.paymentMethod === 'credit-card') {
      const paymentMethod = row.insertCell(0)
      const accountName = row.insertCell(1)
      const cardNumber = row.insertCell(2)
      const expirationDate = row.insertCell(3)
      const securityCode = row.insertCell(4)
      accountName.innerHTML = paymentInformation.accountName
      cardNumber.innerHTML = paymentInformation.cardNumber
      expirationDate.innerHTML = paymentInformation.expirationDate
      paymentMethod.innerHTML = paymentInformation.paymentMethod === 'credit-card' ? 'Credit Card' : 'ACH'
      securityCode.innerHTML = paymentInformation.securityCode
    } else if (paymentInformation.paymentMethod === 'ach') {
      const paymentMethod = row.insertCell(0)
      const accountNumber = row.insertCell(1)
      const routingNumber = row.insertCell(2)
      const accountName = row.insertCell(3)
      paymentMethod.innerHTML = paymentInformation.paymentMethod === 'credit-card' ? 'Credit Card' : 'ACH'
      accountNumber.innerHTML = paymentInformation.accountNumber
      routingNumber.innerHTML = paymentInformation.routingNumber
      accountName.innerHTML = paymentInformation.accountName
    }
  }
}

async function handleFileComplaint () {
  event.preventDefault()
  const form = document.getElementById('complaint-form')
  await fetch('/file-complaint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      subject: form.elements[0].value,
      message: form.elements[1].value,
      status: 'pending'
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
      window.location.href = '/file-complaint'
    }
  })
}

function generateRoomTable () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  const rooms = userData.rooms
  for (let i = 0; i < rooms.length; i++) {
    const room = rooms[i]
    const table = document.getElementById('room-table')
    const row = table.insertRow()
    const name = row.insertCell(0)
    const type = row.insertCell(1)
    const actions = row.insertCell(2)
    name.innerHTML = room.name
    type.innerHTML = room.type
    actions.innerHTML = '<button class="remove-room-btn">Remove Room</button>'
    actions.querySelector('.remove-room-btn').addEventListener('click', function () {
      handleRemoveRoom(room.name)
    })
  }
}

async function handleCreateRoom (event) {
  event.preventDefault()
  const form = document.getElementById('room-form')
  await fetch('/create-room', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: form.elements[0].value,
      type: form.elements[1].value
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
      window.location.href = '/edit-rooms'
    }
  })
}

async function handleRemoveRoom (name) {
  await fetch('/remove-room', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      name: name
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
      window.location.href = '/edit-rooms'
    }
  })
}

function generateComplaintsTable () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  const complaints = userData.complaints
  for (let i = 0; i < complaints.length; i++) {
    const complaint = complaints[i]
    const table = document.getElementById('complaint-table')
    const row = table.insertRow()
    const subject = row.insertCell(0)
    const message = row.insertCell(1)
    const status = row.insertCell(2)
    const actions = row.insertCell(3)
    subject.innerHTML = complaint.subject
    message.innerHTML = complaint.message
    status.innerHTML = complaint.status
    actions.innerHTML = complaint.status === 'pending' ? '<button class="respond-to-complaint-btn">Respond to Complaint</button>' : ''
    if (complaint.status === 'pending') {
      actions.querySelector('.respond-to-complaint-btn').addEventListener('click', function () {
        openRespondToComplaintModal(complaint.id, complaint.subject, complaint.message)
      })
    }
  }
}

function openRespondToComplaintModal (id, subject, message) {
  const modal = document.getElementById('respond-to-complaint-modal')
  modal.style.display = 'block'
  const complaintId = document.getElementById('id')
  complaintId.value = id
  complaintId.style.display = 'none'
  const complaintSubject = document.getElementById('complaint-subject')
  complaintSubject.innerHTML = 'Subject: ' + subject
  const complaintMessage = document.getElementById('complaint-message')
  complaintMessage.innerHTML = 'Message: ' + message
  document.getElementById('close-modal-btn').addEventListener('click', function () {
    modal.style.display = 'none'
  })
}

function handleRespondToComplaint (event) {
  const form = document.getElementById('respond-to-complaint-form')
  const complaintId = document.getElementById('id')
  fetch('/respond-to-complaint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id: complaintId.value,
      response: form.elements[0].value
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
      window.location.href = '/view-complaints'
    }
  })
}

function addRoomsToSwitcher () {
  const roomSelect = document.getElementById('room')
  const userData = JSON.parse(localStorage.getItem('userData'))
  const rooms = userData.rooms
  for (let i = 0; i < rooms.length; i++) {
    const room = rooms[i]
    const option = document.createElement('option')
    option.value = room.name
    option.text = room.name
    option.innerHTML = room.name
    roomSelect.add(option)
  }
}

function generateMeetingTableDayView () {
  const userData = JSON.parse(localStorage.getItem('userData'))
  let meetings = userData.meetings
  const table = document.getElementById('day-table')
  const roomFilter = document.getElementById('room')
  if (roomFilter.value !== 'all') {
    meetings = meetings.filter(meeting => meeting.meetingRoom === roomFilter.value)
  }
  for (let i = 0; i < meetings.length; i++) {
    const meeting = meetings[i]
    // If meeting is today, add to table. Replace / with - and format is YYYY-MM-DD for today's date
    if (meeting.meetingDate === new Date().toISOString().slice(0, 10).replace(/-/g, '-')) {
      const row = table.insertRow()
      const time = row.insertCell(0)
      const room = row.insertCell(1)
      const organizer = row.insertCell(2)
      const attendees = row.insertCell(3)
      const actions = row.insertCell(4)
      time.innerHTML = meeting.meetingTime
      room.innerHTML = meeting.meetingRoom
      organizer.innerHTML = meeting.organizer
      attendees.innerHTML = meeting.attendees
      actions.innerHTML = '<button class="remove-meeting-btn">Remove Meeting</button>'
      actions.querySelector('.remove-meeting-btn').addEventListener('click', function () {
        handleRemoveMeeting(meeting.id)
      })
    }
  }
}

function handleRoomSwitcherChange () {
  // Clear all non header rows
  const dayTable = document.getElementById('day-table')
  for (let i = dayTable.rows.length - 1; i > 0; i--) {
    dayTable.deleteRow(i)
  }
  const weekTable = document.getElementById('week-table')
  for (let i = weekTable.rows.length - 1; i > 0; i--) {
    weekTable.deleteRow(i)
  }
  generateMeetingTableDayView()
  generateMeetingTableWeekView()
}

function handleDayOrWeek () {
  const dayOrWeek = document.getElementById('day-or-week')
  if (dayOrWeek.value === 'day') {
    document.getElementById('day-table').style.display = 'block'
    document.getElementById('week-table').style.display = 'none'
  } else {
    document.getElementById('day-table').style.display = 'none'
    document.getElementById('week-table').style.display = 'block'
  }
}

function handleRemoveMeeting (id) {
  fetch('/remove-meeting', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      id
    })
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
      window.location.href = '/admin-view-meetings'
    }
  })
}

function generateMeetingTableWeekView () {
  const table = document.getElementById('week-table')
  const roomFilter = document.getElementById('room')
  const userData = JSON.parse(localStorage.getItem('userData'))
  let meetings = userData.meetings

  // Filter the meetings based on the room selection
  if (roomFilter.value !== 'all') {
    meetings = meetings.filter(meeting => meeting.meetingRoom === roomFilter.value)
  }

  // Generate rows for each hour, as done previously
  for (let i = 9; i <= 17; i++) {
    const row = table.insertRow()
    row.insertCell(0).innerHTML = i + ':00'
    for (let j = 1; j <= 5; j++) {
      row.insertCell(j).innerHTML = '<div class="week-day-cell"></div>'
    }
  }

  // Populate the table with filtered meetings for the week
  for (let i = 0; i < meetings.length; i++) {
    const meeting = meetings[i]
    const meetingDate = new Date(meeting.meetingDate)
    const meetingDay = meetingDate.getDay()
    if (meetingDay < 1 || meetingDay > 5) continue

    const meetingTime = meeting.meetingTime.split(':')
    const meetingHour = parseInt(meetingTime[0], 10)
    if (meetingHour < 9 || meetingHour > 17) continue

    const meetingRow = table.rows[meetingHour - 9]
    const meetingCell = meetingRow.cells[meetingDay]
    const meetingInfo = 'Room: ' + meeting.meetingRoom + ' | Organizer: ' + meeting.organizer + ' | Attendees: ' + meeting.attendees

    if (meetingCell.innerHTML.includes('week-day-cell')) {
      meetingCell.innerHTML = meetingInfo
    } else {
      meetingCell.innerHTML += '<br>' + meetingInfo
    }
  }
}

function generateUpdateBillingTable(){
  const userData = JSON.parse(localStorage.getItem('userData'))
  const users = userData.users
  const table = document.getElementById('billing-table')

  for (let i = 0; i < Object.keys(users).length; i++) {
    const row = table.insertRow()
    row.setAttribute('username', users[Object.keys(users)[i]].username)
    const username = row.insertCell(0)
    const firstName = row.insertCell(1)
    const lastName = row.insertCell(2)
    const paymentMethod = row.insertCell(3)
    const accountNumber = row.insertCell(4)
    const routingNumber = row.insertCell(5)
    const accountName = row.insertCell(6)
    const cardNumber = row.insertCell(7)
    const expirationDate = row.insertCell(8)
    const securityCode = row.insertCell(9)
    const actions = row.insertCell(10)
    const user = users[Object.keys(users)[i]]

    username.innerHTML = user.username
    firstName.innerHTML = user.firstName
    lastName.innerHTML = user.lastName

    if (user.paymentInformation === undefined) {
      paymentMethod.innerHTML = '<input type="text" value="N/A">'
      accountNumber.innerHTML = '<input type="text" value="N/A">'
      routingNumber.innerHTML = '<input type="text" value="N/A">'
      accountName.innerHTML = '<input type="text" value="N/A">'
      cardNumber.innerHTML = '<input type="text" value="N/A">'
      expirationDate.innerHTML = '<input type="text" value="N/A">'
      securityCode.innerHTML = '<input type="text" value="N/A">'
    } else {
      paymentMethod.innerHTML = `<input type="text" name="paymentMethod" value="${user.paymentInformation.paymentMethod || 'N/A'}">`
      accountNumber.innerHTML = `<input type="text" name="accountNumber" value="${user.paymentInformation.accountNumber || 'N/A'}">`
      routingNumber.innerHTML = `<input type="text" name="routingNumber" value="${user.paymentInformation.routingNumber || 'N/A'}">`
      accountName.innerHTML = `<input type="text" name="accountName" value="${user.paymentInformation.accountName || 'N/A'}">`
      cardNumber.innerHTML = `<input type="text" name="cardNumber" value="${user.paymentInformation.cardNumber || 'N/A'}">`
      expirationDate.innerHTML = `<input type="text" name="expirationDate" value="${user.paymentInformation.expirationDate || 'N/A'}">`
      securityCode.innerHTML = `<input type="text" name="securityCode" value="${user.paymentInformation.securityCode || 'N/A'}">`
    }
    actions.innerHTML = '<button class="update-billing">Update Billing</button>'
    actions.querySelector('.update-billing').addEventListener('click', function () {
      handleUpdateBilling(user.username)
    })
  }
}

function handleUpdateBilling (username) {
  // Get the values of all input fields
  const row = document.querySelector(`[username="${username}"]`)
  const paymentMethod = row.querySelector('[name="paymentMethod"]').value
  const accountNumber = row.querySelector('[name="accountNumber"]').value
  const routingNumber = row.querySelector('[name="routingNumber"]').value
  const accountName = row.querySelector('[name="accountName"]').value
  const cardNumber = row.querySelector('[name="cardNumber"]').value
  const expirationDate = row.querySelector('[name="expirationDate"]').value
  const securityCode = row.querySelector('[name="securityCode"]').value
  let paymentInformation
  if (paymentMethod === 'ach') {
    paymentInformation = {
      paymentMethod,
      accountNumber,
      routingNumber,
      accountName
    }
  } else if (paymentMethod === 'credit-card') {
    paymentInformation = {
      accountName,
      paymentMethod,
      cardNumber,
      expirationDate,
      securityCode
    }
  }

  const data = {
    username,
    paymentInformation
  }

  // Send a POST request to update the billing information
  fetch('/update-billing', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(response => {
    if (response.status === 200) {
      response.json().then(data => {
        localStorage.setItem('userData', JSON.stringify(data.userData))
      })
      window.location.href = '/update-billing'
    }
  })
}
