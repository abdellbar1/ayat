import re

html_text = """<html><head>
    <meta http-equiv="Content-Type" content="text/html; charset=windows-1256">
    <title>نتائج البحث</title>
    <meta http-equiv="CACHE-CONTROL" content="NO-CACHE">
    <meta http-equiv="EXPIRES" content="-1">
    <meta http-equiv="PRAGMA" content="NO-CACHE">
    <!-- meta name="viewport" content="width=device-width, initial-scale=1.0" -->
    <link rel="stylesheet" href="../holyquran.css" type="text/css" media="screen">
    <script async="" src="https://www.google-analytics.com/analytics.js"></script><script language="JavaScript">
    <!-- Begin
    var on = new Array(20);
    
    for (i = 0; i < 20; i++)
    {
        on[i] = true;
    }
    
    function showEnglish(chapter, verse, on)
    {
        var tdVerseId, tdSepId;
        tdSepId = chapter + "-" + verse + "-1";
        tdVerseId = chapter + "-" + verse;
        if(on)
        {
            document.all.item(tdSepId).style.display = "";
            document.all.item(tdVerseId).style.display = "";
        }
        else
        {
            document.all.item(tdSepId).style.display = "none";
            document.all.item(tdVerseId).style.display = "none";
        }   
        return(!on);
    }

    function formHandler(site)
    {
        //var URL = site.options[site.options.selectedIndex].value;
        var index = document.all.item(site).options.selectedIndex;
        var URL =  document.all.item(site).options[index].value;
        document.location.href = URL;
    }
    function GetCookie(c_name)
    {
        if (document.cookie.length>0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start!=-1)
            { 
                c_start = c_start + c_name.length + 1; 
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start, c_end));
            } 
        }
        return "";
    }
    var heartPumpSeconds;
    function SaveVerse(sura, ayah, num)
    {
        var cookie_date = new Date ( 2150, 01, 15 );
        var savedVerses = GetCookie("savedVerses");
        var suraVerse = sura + ":" + ayah;
        var re, emptyVerses;
        
            // Save the verse, and set the value and image
        if (document.getElementById("save" + num).value == '')
        {
            if (savedVerses == "")
            {
                savedVerses = suraVerse;
                document.cookie = "savedVerses=" + escape(savedVerses) + ";expires=" + cookie_date.toGMTString() + ";path=/";
            }
            else if (savedVerses.indexOf(suraVerse) == -1)
            {
                    // Count the number of verses, and truncate last verse if greater than or equal to 30
                re = /[0-9]*/g;
                emptyVerses = savedVerses.replace(re, '');
                re = /,/g;
                emptyVerses = emptyVerses.replace(re, '');
                if (emptyVerses.length >= 30)
                {
                    re = /,[0-9]*:[0-9]*$/;
                    savedVerses = savedVerses.replace(re, '');
                }
                savedVerses = suraVerse + "," + savedVerses;
                document.cookie = "savedVerses=" + escape(savedVerses) + ";expires=" + cookie_date.toGMTString() + ";path=/";
            }
            document.getElementById("save" + num).src = "../images/newimages/gotverse.gif";
            document.getElementById("save" + num).value = 'saved';
            heartPumpSeconds = 0;
            closeInterval = window.setInterval('PumpHeart()', 100);

        }
        else
        {
            var replaceString = new RegExp(suraVerse + ",|," + suraVerse + "|" + suraVerse);
            savedVerses = savedVerses.replace(replaceString, '');
            document.cookie = "savedVerses=" + escape(savedVerses) + ";expires=" + cookie_date.toGMTString() + ";path=/";
            document.getElementById("save" + num).src = "../images/newimages/addverse.gif";
            document.getElementById("save" + num).value = '';
        }

    }

    if (document.images) 
    {
         heartpump = new Image
         heartstop = new Image
         heartpump.src = "../images/newimages/heartpump.gif";
         heartstop.src = "../images/newimages/portfolio.gif";
    }   

    function PumpHeart()
    {
        heartPumpSeconds++;
        if (heartPumpSeconds <= 30)
        {
            document.getElementById("portfolioImg").src = heartpump.src;
        }
        else
        {
            clearInterval(closeInterval);
            closeInterval = '';
            document.getElementById("portfolioImg").src = heartstop.src;
        }
    }
    function DisplayUnDisplayInfo(id)
    {
        if (document.all.item(id).style.display == "none")
        {
            document.all.item(id).style.display = "";
        }
        else
        {
            document.all.item(id).style.display = "none";
        }
    }
    // End -->
    </script>
    <script language="javascript1.2" src="../scripts/clicksearch.js"></script>
    </head>
    <body bgcolor="#FFFFFF" data-new-gr-c-s-check-loaded="14.1167.0" data-gr-ext-installed="">
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-100424381-1', 'auto');
      ga('send', 'pageview');

    </script>

    <div align="center">
    <script async="" src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
    <!-- Holy Quran Search Pages -->
    <ins class="adsbygoogle" style="display:inline-block;width:728px;height:90px" data-ad-client="ca-pub-1969388177942767" data-ad-slot="6153612611"></ins>
    <script>
    (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    </div>
    
    <div align="center"><center>
    <table dir="rtl" border="0" width="600" cellpadding="2">
    <tbody><tr>
        <td bgcolor="#05bf8b" colspan="4" align="center">
        <table dir="rtl" width="100%" bgcolor="#ffffff">
            <tbody><tr>
            <td>
                <p align="Right"><font size="4" face="Arabic Transparent">كلمة البحث:  أَمْ<br>عدد الآيات التي وجدت فيها كلمة التنقيب لهذه الصفحة هي: 20<br>عدد الكلمات المنقّبة عنها في الآيات لهذه الصفحة: 23<br>الجذور المتوفرة هي: ءم - <a href="qsearch.pl?st=%c7%e3&amp;sr=%c1%e3%e3&amp;sc=1&amp;sv=0&amp;ec=114&amp;ev=0&amp;ae=a&amp;mw=r&amp;alef=ON&amp;br=yes">ءمم</a> 
                </font></p>
            </td>
                <td bgcolor="#ffffff"><a href="../docs/doubleclicksearch.html"><img border="0" src="../images/newimages/doubleclicksearch.jpg" alt="انقر مرتين (Double Click) على الكلمة لتبحث عنها"></a></td>
            </tr>
        </tbody></table>
        </td>
    </tr>"""

# Remove all HTML tags
#plain_text = re.sub(r'<[^>]*>', '', html_text)

# Count the number of characters
num_characters = len(html_text)

print("Number of characters:", num_characters)
