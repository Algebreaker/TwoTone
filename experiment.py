from psychopy import visual, core, event, gui
import os
import random
import csv

# Step 1: Ask for participant ID
exp_info = {'Participant ID': ''}
dlg = gui.DlgFromDict(dictionary=exp_info, title="Experiment")
if not dlg.OK:
    core.quit()

# Step 2: Define path to the folder containing all images
image_folder = '/home/johanna/Documents/MooneyImags/images'  # Folder with original images
template_folder = '/home/johanna/Documents/MooneyImags/templates'  # Folder with template images

# Initialize window with a larger size
win = visual.Window([1600, 1600], color='black')

# Initialize text components
question1_text = visual.TextStim(win, text="Can you see what this is? (y/n)", color='white', pos=(0, -0.7))
question2_text = visual.TextStim(win, text="How clear is the image? (1-5)", color='white', pos=(0, -0.7))

# Increase the image size while keeping it square
image_size = (0.9, 0.9)  # Square size (width, height) in normalized units (relative to window size)

# Function to present image and ask question
def present_image_and_ask_question(image, question_text):
    img_stim = visual.ImageStim(win, image=image, pos=(0, 0.2), size=image_size)
    img_stim.draw()
    question_text.draw()
    win.flip()
    keys = event.waitKeys(keyList=['y', 'n', '1', '2', '3', '4', '5'])
    return keys[0]  # Return the first key pressed

# Load all images
all_images = sorted([img for img in os.listdir(image_folder) if img.endswith('.png') or img.endswith('.jpg')])

# Shuffle images and split into three blocks
random.shuffle(all_images)
n_images_per_block = len(all_images) // 3

blocks = [all_images[i:i + n_images_per_block] for i in range(0, len(all_images), n_images_per_block)]

# Ensure that we only have three blocks
blocks = blocks[:3]

# Prepare to collect data
all_responses = []

# Step 3: Loop through each block and present images
for block_num, block_images in enumerate(blocks, start=1):
    responses = []
    
    # Block introduction
    intro_text = visual.TextStim(win, text=f"Block {block_num}\nPress any key to start.", color='white', pos=(0, 0))
    intro_text.draw()
    win.flip()
    event.waitKeys()
    
    # Present images and ask if they can see what this is
    for img_name in block_images:
        img_path = os.path.join(image_folder, img_name)
        initial_response = present_image_and_ask_question(img_path, question1_text)
        responses.append({
            'block': block_num,
            'image': img_name,
            'initial_response': initial_response,
            'final_response': '',  # Placeholder for final response
            'clarity': ''  # Placeholder for clarity rating
        })

    # Fade between original images and template images, both ways
    for img_name in block_images:
        img_path = os.path.join(image_folder, img_name)
        template_img_name = img_name.replace('.png', '_template.png').replace('.jpg', '_template.jpg')
        template_img_path = os.path.join(template_folder, template_img_name)

        if os.path.exists(template_img_path):
            img_stim = visual.ImageStim(win, image=img_path, pos=(0, 0.2), size=image_size)
            template_stim = visual.ImageStim(win, image=template_img_path, pos=(0, 0.2), size=image_size)

            for _ in range(3):
                # Fade from image to template
                for fade in range(0, 101, 5):  # Fade in from 0 to 100% opacity
                    alpha = fade / 100.0
                    img_stim.setOpacity(1 - alpha)
                    template_stim.setOpacity(alpha)
                    img_stim.draw()
                    template_stim.draw()
                    win.flip()
                    core.wait(0.05)

                core.wait(5)

                # Fade from template back to image
                for fade in range(0, 101, 5):  # Fade out from 100% opacity
                    alpha = fade / 100.0
                    img_stim.setOpacity(alpha)
                    template_stim.setOpacity(1 - alpha)
                    img_stim.draw()
                    template_stim.draw()
                    win.flip()
                    core.wait(0.05)

                core.wait(5)

    # Present images again and ask about clarity
    for i, img_name in enumerate(block_images):
        img_path = os.path.join(image_folder, img_name)
        final_response = present_image_and_ask_question(img_path, question1_text)
        clarity_response = present_image_and_ask_question(img_path, question2_text)
        responses[i]['final_response'] = final_response
        responses[i]['clarity'] = clarity_response
    
    # Store block responses
    all_responses.extend(responses)

# Step 4: Save all responses to CSV
output_file = f'data/{exp_info["Participant ID"]}_responses.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Participant ID', 'Block', 'Image', 'Initial Response', 'Final Response', 'Clarity'])
    for response in all_responses:
        writer.writerow([exp_info['Participant ID'], response['block'], response['image'], response['initial_response'], response['final_response'], response['clarity']])

# Clean up
win.close()
core.quit()






