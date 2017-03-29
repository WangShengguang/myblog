$(document).ready(function () {
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            //done方法就是上传完毕的回调函数，其他回调函数可以自行查看api
            //注意result要和jquery的ajax的data参数区分，这个对象包含了整个请求信息
            //返回的数据在result.result中，假设我们服务器返回了一个json对象
            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo(document.body);
            });
            //重新setoPtion(); 用从文件提取的数据画图
        }
    });

    //进度条
    $('#fileupload').fileupload({
        /* ... */
        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $('#progress .bar').css(
                'width',
                progress + '%'
            );
        }
    });

    /*
     var ip='';
     $.get('/ip/'+ip).done(function(data){

     })
     */
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('main'));

    $.get('/lfj/api/zone_data/').done(function (data) {
        console.log(data);
        // 指定图表的配置项和数据
        //折线图
        option = {
            title: {
                text: '从南到北各县百岁老人人数',
                // subtext: '访问次数'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['访问量']
            },
            toolbox: {
                show: true,
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    dataView: {readOnly: false},
                    magicType: {type: ['line', 'bar']},
                    restore: {},
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: data.zone//['周一', '周二', '周三', '周四', '周五', '周六', '周日']   //时间 从api获取
            },
            yAxis: {
                type: 'value',
                axisLabel: {
                    formatter: '{value} '
                }
            },
            series: [
                {
                    name: '访问量',
                    type: 'line',
                    data: data.count//[1, -2, 2, 5, 3, 2, 0],   //访问量  从api获取
                }
            ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    });


});