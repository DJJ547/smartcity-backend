from ultralytics import YOLO

model = YOLO('./models/best.pt')
model2 = YOLO('./models/Emr&Incident_Model_V11_best.pt')

def detect(img, incident=False):
    if incident:
        results = model2(img)
    else:
        results = model(img)
        
    results_list = []
    for result in results:
        if len(result.boxes.cls)>0:
            for i in range(len(result.boxes.cls)):
                confidence = result.boxes.conf[i].item()
                if incident and confidence < 0.8:
                    break
                label_id = int(result.boxes.cls[i].item())
                label = result.names[label_id]
                position = result.boxes.xyxy[i].tolist()
                result_data = {'label': label, 'confidence': confidence, 'position': position}
                results_list.append(result_data)
    return results_list

if __name__ == '__main__':
    img = 'https://t3.ftcdn.net/jpg/02/35/84/28/360_F_235842874_V3avvzfQPeHypw9eVCbSUGxOMmZW7jDT.jpg'
    results = detect(img)
    print(results)
