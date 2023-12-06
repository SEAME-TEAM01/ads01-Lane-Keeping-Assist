# ------------------------------------------------------
# Import library
import  os
import  json
import  pygame
from    utils.prints \
        import  *

# ------------------------------------------------------
# LabelSaver Class
class   DatasetSaver():
    def __init__(self, h_samples, label_dir, label_file, image_dir):
        self.h_samples  = h_samples
        self.label_dir  = label_dir
        self.label_file = label_file
        self.image_dir  = image_dir
    
        self.index = 0

        folder = os.path.dirname(self.label_file)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        if os.path.exists(self.label_file):
            os.remove(self.label_file)

        self.label_file = open(self.label_file, 'a')

        print_info("VehicleManager initialize done")
        print_end()
        

    def save(self, display, x_lanes_list):
        image_file = self.image_dir + f'{self.index:04d}' + '.jpg'
        folder = os.path.dirname(image_file)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        if os.path.exists(image_file):
            os.remove(image_file)

        filestring = {
            "lanes_x": x_lanes_list,
            "lane_y": self.h_samples,
            "image_name": image_file}
        jsonstring = json.dumps(filestring)
        self.label_file.write(jsonstring + '\n')

        pygame.image.save(display, f"{image_file}")

        self.index += 1

    def close_file(self):
        self.label_file.close()