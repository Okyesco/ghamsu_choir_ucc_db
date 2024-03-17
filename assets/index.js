// Update this array with the paths to your images
const imageSources = [
    'path/to/image1.jpg',
    'path/to/image2.jpg',
    'path/to/image3.jpg',
];

// Function to set a random background image
function setRandomBackground() {
    const imageContainer = document.getElementById('imageContainer');
    const randomIndex = Math.floor(Math.random() * imageSources.length);
    const imageUrl = imageSources[randomIndex];

    imageContainer.style.backgroundImage = `url(${imageUrl})`;
}

// Call the function to set an initial background
setRandomBackground();