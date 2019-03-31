# coding: utf-8
#
# This plugin identifies faces from fkvideo_detector and saves the identification results to a static HTML file.
#
import base64
import io
import psycopg2
from facenapi.server.base_video_handler import BaseVideoHandler


def activate(app, ctx, options):
    output = open('/home/user/public_html/found.html', 'w')
    print('<style> img { max-width: 100px; max-height: 100px; } </style><table><tr><td>Needle</td><td>Found</td></tr>',
          file=output)
    output.flush()

    class DemoHandler(BaseVideoHandler):

        async def process_frame(self, *args, image, faces, timestamp, detector_info, **kwargs):
            with self.timeit('nnapi'):
                ## 'nnapi' is a log key which indicates the default facen extractor response time
                await self.ctx.extractor.enrich(faces, facen=True)
            for face in faces:
                results = await self.ctx.faces.identify(self.user, 'Allow', face, limit=1, threshold=0.75)
                thumb_rect = image.shape.intersect(face.bbox)
                thumb_img = image.img.crop((thumb_rect.left, thumb_rect.top, thumb_rect.right, thumb_rect.bottom))
                thumb_contents = io.BytesIO()
                thumb_img.save(thumb_contents, format='JPEG', quality=80)
                thumb_contents.seek(0)

                print('<tr><td><img src="data:image/jpeg;base64,%s" /></td>' % base64.b64encode(
                    thumb_contents.getvalue()).decode(), file=output)
                print('<td>', file=output)
                # print(results, file=output)
                for result in results:

                    # print(result.confidence, file=output)
                    # print('<hr>', file=output)
                    face_meta = result.face['meta']
                    # face_cam_id = result.face['cam_id']
                    face_gallery = result.face['gallery']
                    face_timestamp = result.face['timestamp']
                    face_photo = result.face['photo']
                    face_thumbnail = result.face['thumbnail']
                    face_confidence = result.confidence
                    face_id = result.face['_id']

                    log_event(face_id, face_confidence, face_meta, face_thumbnail, face_photo)
                    print('<img src="%s" />' % face_thumbnail, file=output)
                    print(
                        '<a href="%s">"Full frame" </a> | User id: %s, Date: %s, Confidence: %s, Gallery: %s, Meta: %s' %
                        (face_photo,
                         face_id,
                         face_timestamp,
                         face_confidence,
                         face_gallery,
                         face_meta),
                        file=output
                    )
                print('</td></tr>', file=output)
                output.flush()

    app.add_handlers('.*', [
        ('/static-demo/frame', DemoHandler),
    ])

    def log_event(id_, confidence, meta, thumbnail, photo):
        params = {
            'dbname': 'entrance',
            'user': 'postgres',
            'password': 'qweasdzxc',
            'host': '100.100.148.215',
            'port': 5432
        }

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        allow_key = 0
        if meta == 'deny_':
            allow_key = 6
        elif meta == 'allow_':
            allow_key = 1
        else:
            allow_key = 1
        cur.execute("SELECT log.log_entrance_cam(%s, %s, %s, %s, %s, %s)",
                    (str(allow_key), str(id_), str(thumbnail), meta, photo, str(confidence)))
        print(cur.fetchone())
        conn.commit()
        cur.close()
        conn.close()

# ['photo_hash', 'facen', 'x1', 'detector_info', 'gallery', 'y2', 'meta', 'normalized', 'person_id', 'cam_id', '_id', 'x2', 'y1', 'photo', 'friend', 'timestamp', 'owner', 'thumbnail']
