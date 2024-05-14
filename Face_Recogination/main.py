import os,pickle,random,cv2,face_recognition,pandas as pd,numpy as np
from pathlib import Path
import Face_Recogination.xog as xog
db=xog.Data()
db.create_table()
class Main:
    def __init__(self,
                 ddir="media/dataset/image/",data="media/dataset/data/",
                 test="media/dataset/test/"):
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Add more extensions if needed
        self.ddir=ddir
        self.folder_path=""
        self.data=data
        self.test=test



    def rename_files(self,folder_path="media/dataset/check/"):
        self.folder_path=folder_path
        if  os.path.exists(self.folder_path):
            try:
                os.makedirs(self.ddir)
                os.makedirs(self.data)
                os.makedirs(self.test)
            except:
                pass
        self.image_files = []
        for file_name in os.listdir(self.folder_path):
            if os.path.isfile(os.path.join(self.folder_path, file_name)):
                _, extension = os.path.splitext(file_name)
                if extension.lower() in self.image_extensions:
                    self.image_files.append(file_name)
                    os.rename(self.folder_path+file_name,self.ddir+str(len(self.image_files))+".jpeg")

    
        return len(self.image_files)
    




    def generate(self):
        self.image_files = []
        for file_name in os.listdir(self.ddir):
            if os.path.isfile(os.path.join(self.ddir, file_name)):
                _, extension = os.path.splitext(file_name)
                if extension.lower() in self.image_extensions:
                    self.image_files.append(file_name)


        first_male = ["Liban", "khadar", "Abas", "suleyman", "Omar", "Abdullahi"]
        first_female = ["khadro", "sacdiyo", "xalimo", "caasho", "safiyo", "ruweydo"]
        second_names = ["Yaxye", "mohamed", "Axmed", "Maxmuud", "Abdiqaadir", "Da'ud"]
        last_names = ["Cali", "Geedi", "Yusuf", "Kaafi", "Abdulle", "Khaalid"]
        fasal = ["CA206", "CA207", "CA209", "CA201", "CA202", "CA205"]
        ID = []
        Name = []
        Class = []
        Images = []
        encode = []

        last_first_male_index = len(first_male) - 1
        last_second_names_index = len(second_names) - 1
        last_last_names_index = len(last_names) - 1
        DEFAULT_ENCODINGS_PATH = Path(self.data+"encodings.pkl")   
        count_test=0
        count_remove=0
        count=0
        if db.count() == None:
            kii=1
        else:
            kii=int(db.count())

        for i in range(len(self.image_files)):
            first = random.randint(0, last_first_male_index)
            second = random.randint(0, last_second_names_index)
            last = random.randint(0, last_last_names_index)
            
            IDga="C11800" + str(i+kii)
            full_name = first_male[first] + " " + second_names[second] + " " + last_names[last]
            Name.append(full_name)
            ID.append("C11800" + str(i))
            Class.append(fasal[last])
            file=self.ddir + self.image_files[i]
            Images.append(file)
            image = face_recognition.load_image_file(file)
            face_encoding = face_recognition.face_encodings(image)
            encode_test=np.array(encode)
            if len(face_encoding) > 0 :
                face_distances = face_recognition.face_distance(encode_test, face_encoding[0])
                matches = face_distances < 0.1
                face_distances_test = face_recognition.face_distance(encode_test, face_encoding[0])
                matches_test = face_distances_test < 0.5
                if np.any(matches):
                    os.rename(file,self.folder_path+str(count)+".jpeg")
                    count+=1
                    Name.pop()
                    ID.pop()
                    Images.pop()
                    Class.pop()
                    db.delete_data(IDga)
                elif np.any(matches_test):
                    os.rename(file,self.test+str(count_test)+".jpeg")
                    Name.pop()
                    ID.pop()
                    Images.pop()
                    Class.pop()
                    db.delete_data(IDga)
                    count_test+=1
                else:
                    encode.append(face_encoding[0])
            else:
                os.remove(file)
                Name.pop()
                ID.pop()
                Images.pop()
                Class.pop()
                db.delete_data(IDga)
                print(f"No face found in {file}")
                count_remove+=1



        name_encodings = {"ID": ID, "encodings": encode}
        with DEFAULT_ENCODINGS_PATH.open(mode="wb") as f:
            pickle.dump(name_encodings, f)
        data = {
            "ID": ID,
            "Name": Name,
            "Class": Class,
            "Image": Images,
        }
        for i in range(len(ID)):
            db.insert_data(ID[i],Name[i],Class[i],6177,str(Images[i]))

        df = pd.DataFrame(data)

        # Specify the file name for the CSV file
        filename = self.data+"dataset.csv"
       
        df.to_csv(filename, index=False)
        return "we catched duplicated images are :"+str(count)+"   ","Same person images are "+str(count_test),"remove images that was not found face are : "+str(count_remove)
        print("we catched duplicated images are : ",count,
              "\nitems and Same person are : ",count_test," images",
              "\nand remove images that was not found face are : ",count_remove," images ")


    def load_data(self):
        # Read pickle data
        pickle_file_path = self.data+"encodings.pkl"
        with open(pickle_file_path, 'rb') as file:
            data = pickle.load(file)
        self.known_face_encodings = data["encodings"]
        self.df = pd.read_csv(self.data+"dataset.csv")
        self.known_face_names = db.get_column("ID ")
        self.image_list = db.get_column("Image ")

    def recognize_face(self,test_image_path, distance_threshold=0.5):
        self.load_data()
        distance_threshold=distance_threshold
        test_image = face_recognition.load_image_file(test_image_path)
        test_face_encodings = face_recognition.face_encodings(test_image)

        if len(test_face_encodings) == 0:
            return "No face found in the test image"

        face_distances = face_recognition.face_distance(self.known_face_encodings, test_face_encodings[0])
        matches = face_distances < distance_threshold
        distance_threshold+=0.1
        if np.any(matches):
            matched_names = np.array(self.known_face_names)[matches].tolist()
            matched_images = np.array(self.image_list)[matches].tolist()
            x=db.search_data(Image=matched_images[0])
            self.present_faces(test_image, matched_images,matched_names)
            # return x
        elif distance_threshold<0.5:
            self.recognize_face(test_image_path,distance_threshold=distance_threshold)
            return ("No match found for the test image.")
            

    def present_faces(self,test_image, matched_images,matched_names):
        cv2.namedWindow('Test Image', cv2.WINDOW_NORMAL)

        # Show the test image in the window
        cv2.imshow(str(matched_names), test_image)

        for matched_image in matched_images:
            matched_image = cv2.imread(matched_image)
            cv2.namedWindow('Matched Image', cv2.WINDOW_NORMAL)

            # Show the matched image in the window
            cv2.imshow('Matched Image', matched_image)

            # Wait for a key press to continue to the next match
            cv2.waitKey(0)

        # Close all windows
        cv2.destroyAllWindows()