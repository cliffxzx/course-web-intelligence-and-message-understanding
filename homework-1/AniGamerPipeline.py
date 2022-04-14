import csv
from elk import elk

class ElasticPipeline:
    def process_item(self, item, spider):
        elk.index(index='danmu', body={
            'color': item['color'],
            'position': item['position'],
            'size': item['size'],
            'sn': item['sn'],
            'text': item['text'],
            'time': item['time'],
            'userid': item['userid'],
            'title': item['title'],
        })
        return item

class CSVPipeline:
    def process_item(self, item, spider):
        with open(r'ani_gamer.csv', 'a', newline='') as csvfile:
            fieldnames = ['color', 'position', 'size', 'sn', 'text', 'time', 'userid', 'title']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() < 100:
                writer.writeheader()

            writer.writerow({
                'color': item['color'],
                'position': item['position'],
                'size': item['size'],
                'sn': item['sn'],
                'text': item['text'],
                'time': item['time'],
                'userid': item['userid'],
                'title': item['title'],
            })

            return item