import base64
import io

import pandas as pd  #时间库
import requests      #Python requests 是一个常用的 HTTP 请求库，可以方便地向网站发送 HTTP 请求，并获取响应结果
import matplotlib.pyplot as plt #matlab中Plot绘图库
from matplotlib.dates import DateFormatter #matplotlib.dates 模块处理日期类型数据
import matplotlib
matplotlib.use('TkAgg')     #多种办法完美解决AttributeError: module ‘backend_interagg‘ has no attribute ‘FigureCanvas‘
from flask import Flask, render_template

app = Flask(__name__)

#方法
#相当于爬虫，爬取图标里的数据
def fetch_data():
    """从API获取数据"""
    url = f'http://8.130.95.237:5000/api/predict'
    response = requests.get(url)
    data = response.json()
    return data #得到JSON格式数据


def fetch_news():
    url = f"https://whyta.cn/api/tx/bulletin?key=96e175d76865";
    responsenews = requests.get(url)
    data = responsenews.json()
    return data #得到JSON格式数据




#这个方法，用来画图，根据数据来画图
#def plot_data(data):


    #plt.show()

@app.route('/')
def main():
    return render_template('index.html')  # 相对路径

@app.route('/bitebi')
def api():
    data = fetch_data()
    datanews = fetch_news()

 #   plot_data(data)
    dates = pd.to_datetime(data['dates'])
    real_high = data['real_H']
    real_low = data['real_L']
    pred_high = data['pred_H']
    pred_low = data['pred_L']
# 得到网站里dates,realh,reall...里面的数据

# 用于生成一个固定频率的DatetimeIndex时间索引，
    future_dates = pd.date_range(start=dates[-1] + pd.Timedelta(days=1), periods=2)
    #
    future_pred_high = data['future_pred_H'][:2]
    #
    future_pred_low = data['future_pred_L'][:2]
    #
    num_pred = len(pred_high)
    dates = dates[-num_pred:]
    real_high = real_high[-num_pred:]
    real_low = real_low[-num_pred:]
    combined_dates = pd.concat([pd.Series(dates), pd.Series(future_dates)])
    combined_pred_high = pred_high + future_pred_high
    combined_pred_low = pred_low + future_pred_low
    combined_real_high = list(real_high) + [None, None]
    combined_real_low = list(real_low) + [None, None]
    plt.figure(figsize=(10, 5))
    plt.plot(combined_dates, combined_real_high, label='Actuall High', color='red')
    plt.plot(combined_dates, combined_real_low, label='Actuall Low', color='blue')
    plt.plot(combined_dates, combined_pred_high, label='Predicted High', linestyle='--', color='orange')
    plt.plot(combined_dates, combined_pred_low, label='Predicted Low', linestyle='--', color='green')
    plt.title('BITCOIN PRICE PREDICTION')
    plt.xlabel('DATE')
    plt.ylabel('PRICE')
    plt.legend()
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()
    img = io.BytesIO()  #创建一个字节流对象，将图像保存到其中。
    #   y = [1, 2, 3, 4, 5]
    #   x = [0, 2, 1, 3, 4]
    #   plt.plot(x, y)
    plt.savefig(img, format='png') #保存绘制数据后创建的图形
    img.seek(0) #在这个序列文件中搜索到给定的帧

    plot_url = base64.b64encode(img.getvalue()).decode()    #将图像数据编码为Base64字符串
    #
    # json = pd.DataFrame(datanews['result'])
    #
    # X = json.iloc[:, 0:61]  # 将0到61列数据赋值给X
    # X = X.values  # .values方法将dataframe转为numpy.ndarray，也可以用np.array(X)将其转为numpy.ndarray
    # json = X.tolist()  # 将X转为list
    #
    # return render_template('bitebi.html', plot_url=plot_url ,json = json)
    return render_template('bitebi.html', plot_url=plot_url)



if __name__ == '__main__':
    app.run()