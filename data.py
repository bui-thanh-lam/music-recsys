class MusicModel:
    def __init__(self,echoID,trackId,trackname,trackpopularity):
        self.music = {'echonest_track_id': echoID,
                 'spotify_track_id':trackId,
                 'track_name': trackname,
                 'artists': [{'artist_id': '',
                              'artist_name': '',
                              'artist_popularity': '',
                              'genres': ['', '']
                              },
                             {'artist_id': '',
                              'artist_name': '',
                              'artist_popularity': '',
                              'genres': ['', '']
                              }],
                 'track_popularity': trackpopularity}
class Database:
    def __init__(self):
        self.list_music = ["Khắp xung quanh", "Không làm gì", "Cho tôi đi theo", "Xanh"
    , "Cho tôi lang thang", "Cho", "Em dạo này", "Bartender", "Lần cuối (đi bên em xót xa người ơi)",
              "Chuyển kênh (sản phẩm này không phải là thuốc)"
    , "Mếu máo (T.T)", "(tôi) Đi trú đông", "Hết thời", "Tìm người nhà"]
    def get_history(self,ID):
        data=[]
        for i in range(len(self.list_music)):
            m=MusicModel(i,i,self.list_music[i],i)
            data.append(m.music)
        return {"data":data}
    def get_recommend_play_list(self,ID):

        data = []
        for i in range(5):
            recommend_list=[]
            for j in range(len(self.list_music)):

                m = MusicModel(j, j, self.list_music[j], j)
                recommend_list.append(m.music)
            data.append({'playlist':
                             recommend_list})
        
        return {"data": data}


    def login(self,username,password):

        return {'user_id': '000ebc858861aca26bac9b49f650ed424cf882fc',
                'user_name': 'giang',
                'pass_word': '123',
                'name': 'Bui Truong Giang','login':True}

    def search(self,trackname):
        recommend_list = []
        
        for i in range(len(self.list_music)):
            if(trackname in self.list_music[i]):
                m = MusicModel(i, i, self.list_music[i], i)
                recommend_list.append(m.music)
        return {"data":recommend_list}
    
    def playlistfortrack(self,trackname):
        recommend_list = []
        m = MusicModel(0, 0, trackname, 0)
        recommend_list.append(m.music)
        for i in range(1,len(self.list_music)):
            m = MusicModel(i, i, self.list_music[i], i)
            recommend_list.append(m.music)
        return {"data": recommend_list}
    