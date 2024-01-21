


// Import necessary modules and the Prisma client
const { PrismaClient } = require('@prisma/client');

// Example data to be added
const userData = {
    password: 'admin@PF0',
    firstName: 'Philopateer',
    lastName: 'Azer',
    email: 'admin@patternfinder.com',
};

// Function to add data to the user table
async function addUser() {
  const prisma = new PrismaClient();

  try {
    // Use the create method from the UsersService to add data to the user table
    const newUser = await prisma.users.create({
      data: userData,
    });

    console.log('User added successfully:', newUser);
  } catch (error) {
    console.error('Error adding user:', error.message);
  } finally {
    // Close the Prisma client
    await prisma.$disconnect();
  }
}

// Call the function to add the user
addUser();
