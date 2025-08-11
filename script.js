// Additional JavaScript for the LLM-Picbreeder tutorial

// Function to simulate story generation
function generateStory(prompt) {
    const stories = [
        "Once upon a time, in a land far away, there lived a brave knight who discovered a magical sword that could grant wishes. But with great power came great responsibility, and the knight had to make a choice that would change the kingdom forever.",
        "The old lighthouse keeper had watched the sea for fifty years, but tonight was different. A strange light appeared on the horizon, not from any ship he'd ever seen. As it drew closer, he realized it was a message from another world.",
        "Emma found a dusty journal in her grandmother's attic. Each page contained a recipe, but these weren't for food. They were for creating memories, capturing moments, and preserving the essence of love. She decided to try the first one.",
        "The last library on Earth stood in the center of New York, protected by a force field. Inside, the books whispered secrets to each other in the night. When the power finally failed, they had to find a new way to survive.",
        "In the year 2087, children played with holographic pets. But one girl discovered her 'pet' was actually a lost AI from the old world, trying to remember how to be human again."
    ];
    
    return stories[Math.floor(Math.random() * stories.length)];
}

// Function to simulate community ratings
function getCommunityRating() {
    const ratings = [
        { stars: "★★★★★", value: "4.8/5", count: "32 ratings" },
        { stars: "★★★★☆", value: "4.2/5", count: "24 ratings" },
        { stars: "★★★★★", value: "4.9/5", count: "18 ratings" },
        { stars: "★★★☆☆", value: "3.5/5", count: "15 ratings" },
        { stars: "★★★★☆", value: "4.1/5", count: "27 ratings" }
    ];
    
    return ratings[Math.floor(Math.random() * ratings.length)];
}

// Add interactivity to prompt boxes
document.addEventListener('DOMContentLoaded', function() {
    // Add click events to prompt boxes for expansion
    const promptBoxes = document.querySelectorAll('.prompt-content');
    
    promptBoxes.forEach(box => {
        box.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    });
    
    // Add hover effect to evolution tree nodes
    const nodes = document.querySelectorAll('.node');
    
    nodes.forEach(node => {
        node.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.3)';
            this.style.zIndex = '100';
        });
        
        node.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.zIndex = '1';
        });
    });
    
    // Simulate live rating updates
    setInterval(() => {
        const ratingElements = document.querySelectorAll('.rating-value');
        if (ratingElements.length > 0) {
            const rating = getCommunityRating();
            document.querySelector('.star-rating').textContent = rating.stars;
            document.querySelector('.rating-value').textContent = `${rating.value} (${rating.count})`;
        }
    }, 3000);
});

// Function to add a ripple effect to buttons
function addRippleEffect(e) {
    const button = e.currentTarget;
    const ripple = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    ripple.style.width = ripple.style.height = `${diameter}px`;
    ripple.style.left = `${e.offsetX - radius}px`;
    ripple.style.top = `${e.offsetY - radius}px`;
    ripple.classList.add('ripple');
    
    const rippleContainer = button.querySelector('.ripple-container') || button;
    rippleContainer.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Add ripple effect to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', addRippleEffect);
});