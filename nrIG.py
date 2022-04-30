from multiprocessing.pool import RUN
import profile
from pydoc import Doc
from time import sleep
import re

from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from docutil import DocUtil

import atexit

import threading



RUNNING = True




NON_FOLLOWERS = ['https://www.instagram.com/shahzeb__m/', 'https://www.instagram.com/gngedwardstwestbrom/', 'https://www.instagram.com/iamsindhu.krish/', 'https://www.instagram.com/prestonsikhsewa/', 'https://www.instagram.com/citysikhsociety/', 'https://www.instagram.com/meghnathpillay/', 'https://www.instagram.com/taamara.k/', 'https://www.instagram.com/mmansim/', 'https://www.instagram.com/citypunjabisoc/', 'https://www.instagram.com/gtbgyouthslc/', 'https://www.instagram.com/pardeepanesar/', 'https://www.instagram.com/vegsocbath/', 'https://www.instagram.com/uob_societea/', 'https://www.instagram.com/aishhh.p/', 'https://www.instagram.com/aadhyagovil/', 'https://www.instagram.com/bathindiansoc/', 'https://www.instagram.com/unibathfoodanddrink/', 'https://www.instagram.com/sezhh/', 'https://www.instagram.com/tedx_bathuniversity/', 'https://www.instagram.com/dikshamanupriya/', 'https://www.instagram.com/kaurageousuk/', 'https://www.instagram.com/doctoral_bath/', 'https://www.instagram.com/work4all__/', 'https://www.instagram.com/shivem/', 'https://www.instagram.com/sparikh07/', 'https://www.instagram.com/diyabhojwanii/', 'https://www.instagram.com/uclsikhsoc/', 'https://www.instagram.com/pranayysomani/', 'https://www.instagram.com/tanmay_t/', 'https://www.instagram.com/adarsh_nair/', 'https://www.instagram.com/bath_isoc/', 'https://www.instagram.com/ishxn._p/', 'https://www.instagram.com/anushkcat/', 'https://www.instagram.com/shreya.saravana_x/', 'https://www.instagram.com/raahix/', 'https://www.instagram.com/aastha_lunkad/', 'https://www.instagram.com/ravyaarora_/', 'https://www.instagram.com/amishah_22/', 'https://www.instagram.com/uobindiansoc/', 'https://www.instagram.com/bathalogical/', 'https://www.instagram.com/pavmma/', 'https://www.instagram.com/bathconfessions_/', 'https://www.instagram.com/nishkamswat/', 'https://www.instagram.com/plugtub/', 'https://www.instagram.com/kaurscampuk/', 'https://www.instagram.com/singhscampuk/', 'https://www.instagram.com/dechenjay/', 'https://www.instagram.com/uniofbath/', 'https://www.instagram.com/sikhexpo/', 'https://www.instagram.com/srinithi.26/', 'https://www.instagram.com/aditi702/', 'https://www.instagram.com/ashna_sareen/', 'https://www.instagram.com/pankhu2001/', 'https://www.instagram.com/gaurang_aggarwal/', 'https://www.instagram.com/zee_306/', 'https://www.instagram.com/shourya_83/', 'https://www.instagram.com/pranitc_/', 'https://www.instagram.com/zarinsuchi/', 'https://www.instagram.com/devanshbarathi26/', 'https://www.instagram.com/vanshh.agrawal/', 'https://www.instagram.com/samiyahasanx/', 'https://www.instagram.com/prarthanasabharwal/', 'https://www.instagram.com/somhrit.chanda/', 'https://www.instagram.com/akash_parikh_/', 'https://www.instagram.com/vivaan_9/', 'https://www.instagram.com/harshita0204/', 'https://www.instagram.com/_anushkag/', 'https://www.instagram.com/additeegupta_photography/', 'https://www.instagram.com/abhishek.agarwal12/', 'https://www.instagram.com/chanddnii/', 'https://www.instagram.com/aryan_bahl/', 'https://www.instagram.com/nishita4y/', 'https://www.instagram.com/aneeeeekha/', 'https://www.instagram.com/anand._.ajesh/', 'https://www.instagram.com/tusharkalyan95/', 'https://www.instagram.com/diya_.d/', 'https://www.instagram.com/amitn08/', 'https://www.instagram.com/_.axp/', 'https://www.instagram.com/ri.yaa/', 'https://www.instagram.com/yoshoda_bhatt/', 'https://www.instagram.com/nirek_031202/', 'https://www.instagram.com/bamsanight/', 'https://www.instagram.com/farhaan.u/', 'https://www.instagram.com/harshita2003/', 'https://www.instagram.com/abhinavsharma03/', 'https://www.instagram.com/jaiancpatel/', 'https://www.instagram.com/pav1o_/', 'https://www.instagram.com/priyankshiii/', 'https://www.instagram.com/varun_m8/', 'https://www.instagram.com/shreya._.suri/', 'https://www.instagram.com/diya_awade/', 'https://www.instagram.com/real_seetvn/', 'https://www.instagram.com/ejain_2002/', 'https://www.instagram.com/amnaijaz1/', 'https://www.instagram.com/pathakabhijna/', 'https://www.instagram.com/khushi._.desai/', 'https://www.instagram.com/shehxn/', 'https://www.instagram.com/readingchallengebyzoe/', 'https://www.instagram.com/nuzba_ahmad/', 'https://www.instagram.com/tammysharma_/', 'https://www.instagram.com/abhishek.garud/', 'https://www.instagram.com/devchakrabarti17/', 'https://www.instagram.com/parulsrivastava_11/', 'https://www.instagram.com/ninasardoo/', 'https://www.instagram.com/hannah_bawa/', 'https://www.instagram.com/yathukamal/', 'https://www.instagram.com/gaurav_venkatesh_/', 'https://www.instagram.com/poornima_jm/', 'https://www.instagram.com/siddharth_rthz/', 'https://www.instagram.com/fazal_seth/', 'https://www.instagram.com/ahmed_shareeq/', 'https://www.instagram.com/hazim.zameel/', 'https://www.instagram.com/eashita.dhillon/', 'https://www.instagram.com/hunaid.kanal/', 'https://www.instagram.com/shubham07jain/', 'https://www.instagram.com/aroon.rav1/', 'https://www.instagram.com/misterrishishah/', 'https://www.instagram.com/amirakhan4/', 'https://www.instagram.com/ishaan__patel/', 'https://www.instagram.com/anandsk98/', 'https://www.instagram.com/anunaysinghal/', 'https://www.instagram.com/mkhatwani_/', 'https://www.instagram.com/stepantonio/', 'https://www.instagram.com/mdhv99/', 'https://www.instagram.com/arj_kotecha/', 'https://www.instagram.com/preesharupani/', 'https://www.instagram.com/ro.han_s/', 'https://www.instagram.com/_xadix_/', 'https://www.instagram.com/siddhi_charan/', 'https://www.instagram.com/molly_2103/', 'https://www.instagram.com/danica_mehta/', 'https://www.instagram.com/lathashishagarwal/', 'https://www.instagram.com/khushigogia/', 'https://www.instagram.com/karandharamshi/', 'https://www.instagram.com/shaniya_mistry/', 'https://www.instagram.com/plumerhea/', 'https://www.instagram.com/shortkingsanj/', 'https://www.instagram.com/rheaerinjeri/', 'https://www.instagram.com/srushtishaaah/', 'https://www.instagram.com/zeba.anuff/', 'https://www.instagram.com/sabah.khann/', 'https://www.instagram.com/ritto_johnny/', 'https://www.instagram.com/palakbansal67/', 'https://www.instagram.com/bathpaksoc/', 'https://www.instagram.com/mano_lfc/', 'https://www.instagram.com/devanshi_jhonsa/', 'https://www.instagram.com/purvika_j/', 'https://www.instagram.com/shehij_raina/', 'https://www.instagram.com/rishiarora1999/', 'https://www.instagram.com/mihirc4/', 'https://www.instagram.com/ruqiaosm/', 'https://www.instagram.com/itsharshal/', 'https://www.instagram.com/shijovar/', 'https://www.instagram.com/leahpereira_/', 'https://www.instagram.com/harini__2511/', 'https://www.instagram.com/hetshaaah/', 'https://www.instagram.com/louiemiddle30303/', 'https://www.instagram.com/surajdivakala/', 'https://www.instagram.com/know_tarun/', 'https://www.instagram.com/nimiechandhok/', 'https://www.instagram.com/abhay_madaan/', 'https://www.instagram.com/2407alina/', 'https://www.instagram.com/hemanth__kr/', 'https://www.instagram.com/nehabavejaa/', 'https://www.instagram.com/aaron10alb/', 'https://www.instagram.com/_.manav27/', 'https://www.instagram.com/shivrmistry/', 'https://www.instagram.com/nimsach/', 'https://www.instagram.com/anchitshethia/', 'https://www.instagram.com/linneahjelmlindblad/', 'https://www.instagram.com/rohitsinghjain17/', 'https://www.instagram.com/kaushal._.maniyar/', 'https://www.instagram.com/mahikaxgupta/', 'https://www.instagram.com/asth.a/', 'https://www.instagram.com/iishaponkshe/', 'https://www.instagram.com/sonalihazareesing/', 'https://www.instagram.com/godly_97/', 'https://www.instagram.com/aarshia.chawla/', 'https://www.instagram.com/aravind_mama/', 'https://www.instagram.com/jayeneventspr/', 'https://www.instagram.com/faisalalkhaledi6/', 'https://www.instagram.com/karanveernath19/', 'https://www.instagram.com/harshballani/', 'https://www.instagram.com/mohitbuch/', 'https://www.instagram.com/allantechboii/', 'https://www.instagram.com/sarthaksbansal/', 'https://www.instagram.com/sakshishah2000/', 'https://www.instagram.com/thayir_girl/', 'https://www.instagram.com/tuhnvi/', 'https://www.instagram.com/akankshaa08/', 'https://www.instagram.com/xo.tash.xo/', 'https://www.instagram.com/rishi1994/', 'https://www.instagram.com/khushboojain774/', 'https://www.instagram.com/simranmohnani_/', 'https://www.instagram.com/arunasindiankitchen/', 'https://www.instagram.com/rakshitagoel21/', 'https://www.instagram.com/dana_oshi/', 'https://www.instagram.com/adarsh.bokhoree/', 'https://www.instagram.com/garika_kalyan/', 'https://www.instagram.com/ishaani03/', 'https://www.instagram.com/saachipreetbhatia/', 'https://www.instagram.com/_.camilahh/', 'https://www.instagram.com/bensutton.11/', 'https://www.instagram.com/uobas/', 'https://www.instagram.com/xaairax/', 'https://www.instagram.com/iamaditribhuvan/', 'https://www.instagram.com/divyapoddar1810/', 'https://www.instagram.com/b_inbath/', 'https://www.instagram.com/maitri.29/', 'https://www.instagram.com/intriguinginkling/', 'https://www.instagram.com/monthofeverything/', 'https://www.instagram.com/uobathtaekwondo/', 'https://www.instagram.com/shyni.xo/', 'https://www.instagram.com/saharrohmetra/', 'https://www.instagram.com/prachipowar/', 'https://www.instagram.com/subashiniraj/', 'https://www.instagram.com/vvaidehii/', 'https://www.instagram.com/reya.x/', 'https://www.instagram.com/amankulthia/', 'https://www.instagram.com/divijashah/', 'https://www.instagram.com/riasadarangani/', 'https://www.instagram.com/vpbhangra/', 'https://www.instagram.com/bathabacus/', 'https://www.instagram.com/cuindiasoc/', 'https://www.instagram.com/_udita_/', 'https://www.instagram.com/blessen.783/', 'https://www.instagram.com/kavyagrsuqsjpr/', 'https://www.instagram.com/preetikodesia/', 'https://www.instagram.com/arjun_w/', 'https://www.instagram.com/sneha_36/', 'https://www.instagram.com/amikulkalra/', 'https://www.instagram.com/imperialcollegehindusociety/', 'https://www.instagram.com/bath.entrepreneurs/', 'https://www.instagram.com/uc_saasa/', 'https://www.instagram.com/aartii.g/', 'https://www.instagram.com/soniaklotay_/', 'https://www.instagram.com/_namrata_bhoir_/', 'https://www.instagram.com/indiasocsoton/', 'https://www.instagram.com/nihalkaur/', 'https://www.instagram.com/charlotte_hodkin/', 'https://www.instagram.com/deepak.keshari1/', 'https://www.instagram.com/ashishh_nagpal/', 'https://www.instagram.com/warwickasiansociety/', 'https://www.instagram.com/deeclff_/', 'https://www.instagram.com/uweindiansociety/', 'https://www.instagram.com/nhsf_cardiff/', 'https://www.instagram.com/uobbulb/', 'https://www.instagram.com/ayushiparekh_1998/', 'https://www.instagram.com/veeyannasounds/', 'https://www.instagram.com/ryan._shah._/', 'https://www.instagram.com/ya5hvimodi/', 'https://www.instagram.com/looping_pugilist/', 'https://www.instagram.com/ntusikhsoc/', 'https://www.instagram.com/aberasian_society/', 'https://www.instagram.com/djshindyjuttla/', 'https://www.instagram.com/capturedbyalan/', 'https://www.instagram.com/amankaurdhut/', 'https://www.instagram.com/sayan_skywalker/', 'https://www.instagram.com/vaibhav.j8/', 'https://www.instagram.com/uobwib/', 'https://www.instagram.com/mehakkshah/', 'https://www.instagram.com/nagg.yy/', 'https://www.instagram.com/swezeltakespictures/', 'https://www.instagram.com/bathsalsasociety/', 'https://www.instagram.com/chelsyjose/', 'https://www.instagram.com/guptayashpriya/', 'https://www.instagram.com/evealcock/', 'https://www.instagram.com/annaikaahuja/', 'https://www.instagram.com/_dxrshan/', 'https://www.instagram.com/winnsterz/', 'https://www.instagram.com/nimashgunasekara/', 'https://www.instagram.com/nadine059/', 'https://www.instagram.com/bustoninsta/', 'https://www.instagram.com/notlinal/', 'https://www.instagram.com/goldmansolutionsuk/', 'https://www.instagram.com/pharmacast_bath/', 'https://www.instagram.com/ic.asoc/', 'https://www.instagram.com/khalsa_fostering/', 'https://www.instagram.com/shay_butle.r/', 'https://www.instagram.com/exeterhsoc/', 'https://www.instagram.com/exeterasoc/', 'https://www.instagram.com/bath_acs/', 'https://www.instagram.com/bathuniamnesty/', 'https://www.instagram.com/britishindianmedicassociation/', 'https://www.instagram.com/bathjewishsociety/', 'https://www.instagram.com/mukherjeesanmoy/', 'https://www.instagram.com/devidasdharmadhikari/', 'https://www.instagram.com/hannanagpal/', 'https://www.instagram.com/uobffc/', 'https://www.instagram.com/uniofbathmun/', 'https://www.instagram.com/ericpinto98/', 'https://www.instagram.com/sa.dia3016/', 'https://www.instagram.com/bathracequalitygroup/', 'https://www.instagram.com/bathstar/', 'https://www.instagram.com/rhys_.cox/', 'https://www.instagram.com/khanak.xo/', 'https://www.instagram.com/massagebuddyofficial/', 'https://www.instagram.com/bathmeditationsoc/', 'https://www.instagram.com/bathpaps/', 'https://www.instagram.com/jameson_t98/', 'https://www.instagram.com/bristolhindusoc/', 'https://www.instagram.com/bollynightsbath/', 'https://www.instagram.com/wheelbarrow_inc/', 'https://www.instagram.com/bathnightline/', 'https://www.instagram.com/east.meetswest/', 'https://www.instagram.com/bathlatinamericansoc/', 'https://www.instagram.com/theterracebath_/', 'https://www.instagram.com/imperialindiansoc/', 'https://www.instagram.com/subathsport/', 'https://www.instagram.com/890khushi/', 'https://www.instagram.com/bameconsulting/', 'https://www.instagram.com/asiansoccardiff/', 'https://www.instagram.com/desihive/', 'https://www.instagram.com/nirmi08/', 'https://www.instagram.com/bristolasoc/', 'https://www.instagram.com/ferlapaolo/', 'https://www.instagram.com/stavros1.0/', 'https://www.instagram.com/bathdancesoc/', 'https://www.instagram.com/popuppartiesbath/', 'https://www.instagram.com/ragbath/', 'https://www.instagram.com/mrsinghspizza/', 'https://www.instagram.com/hemkunt_foundation/', 'https://www.instagram.com/weare_sass/', 'https://www.instagram.com/secondbridgebath/', 'https://www.instagram.com/divyakapoor424/', 'https://www.instagram.com/ektainitiative/', 'https://www.instagram.com/imjustimp/', 'https://www.instagram.com/bollywoodnation/', 'https://www.instagram.com/bathsofm/', 'https://www.instagram.com/warwick.icd/', 'https://www.instagram.com/uosindiansoc/', 'https://www.instagram.com/leannemansoor/', 'https://www.instagram.com/asohal93/', 'https://www.instagram.com/a.nushkatiwari/', 'https://www.instagram.com/bathcomedyofficial/', 'https://www.instagram.com/official_ubms/', 'https://www.instagram.com/uniofbath_global/', 'https://www.instagram.com/cu_telugu_soc/', 'https://www.instagram.com/theindiansnextdoor/', 'https://www.instagram.com/edgeartscommunity/', 'https://www.instagram.com/teachfirstbathuni/', 'https://www.instagram.com/echoeventsofficial/', 'https://www.instagram.com/bathuniyoga/', 'https://www.instagram.com/kalindi1122/', 'https://www.instagram.com/nhsfbeds/', 'https://www.instagram.com/krit.i5372/', 'https://www.instagram.com/subathinternational/', 'https://www.instagram.com/connex.events/', 'https://www.instagram.com/avasuri001/', 'https://www.instagram.com/reminisce_events_co/', 'https://www.instagram.com/enactus_bath/', 'https://www.instagram.com/desiclubeventspr/', 'https://www.instagram.com/uobbrandrep/', 'https://www.instagram.com/sa.chinkumar8927/', 'https://www.instagram.com/voltz_bath/']

REQUESTS_SENT = ['ARUSHIGUPTAXX', 'PAUMELLEZOE', 'AAKRITIKEDIA_1411', 'ANNIE_RUDE_', 'PRARTHANASABHARWAL', 'GANALINGAM13TH', '_ANVETTA', 'HARSHITA0204', 'NAMZ.NS', 'PAV1O_', '_NAMRATA_BHOIR_', 'RITIKDOSHI', 'NIMANTHAFERNANDO99', 'ARTHIK._1606', 'EESHABADORIA', 'DEVINA_K30', 'MARIAWRXGHT', 'PALLAVI.PRAKASH', 'SWAYAMM._', 'DIVYAKAPOOR424', 'ESHANIKA16', 'LISENKADSOUZA', 'F.L.A.P.F.L.A.P', 'AKASH_V16', 'NEHA_RAJSHEKAR', 'SIDDHANTFR', 'AMBAREEN_AZHAR', 'ANSH.CH_', 'KHUSHI_Y95', 'GAURAV_VENKATESH_', 'SIDDHARTH_RTHZ', 'NOUSHWEEN', 'JISHMAH', 'NXNDINII_', 'NAVYAKHANNA20', 'ADI_OS17', 'ROHANSSINGHANIA', 'LATHASHISHAGARWAL', 'IFRAH.ARIFF', 'JAYESH_ARORA', 'REEMA_BADIANI', 'JUSTIND_18', 'SRUSHTISHAAAH', 'SANJIV19', 'FAIADSHARIF', 'ISHITA_067', '_NIKHIL.RS._', 'RDS_12', 'ANISHASHARMAXX', 'RITTO_JOHNNY', 'RHEA_SHAH213', 'DIYAVIBHAKAR', 'UKDICHAMODAK', 'PALAKBANSAL67', 'XX.ROSITA.XX', 'RAJHARIA', 'ASHWINDAS14', 'KIMM.LEL', 'MANO_LFC', 'NANDUS____', 'NIVE.LOGES', 'NALINBANSALLL', 'DARSHIII_SHAHH', 'DEVANSHI_JHONSA', 'PURVIKA_J', 'SHEHIJ_RAINA', 'RISHIARORA1999', 'DEFNE.KANSU', 'MIHIRC4', '_HANNAH.MATHEW', 'RIDAMANZAR', 'PARAJ97', 'KINSMAN_10', 'RUQIAOSM', 'MOHAMMED_HAMZA1899', 'REYAN.VORA22', 'VALENTEEEEEENA15', 'ITSHARSHAL', 'SHIJOVAR', 'THEBIGMUS', 'ABHIRAJ_RANA15', 'RHEAMUKHI', 'AJAY0807', 'PRIYAANKA.M', 'HETSHAAAH', 'KRISH_SINGH__', 'ANTZBHD', 'LAZERSHOOTER', 'SHRINIDHI_3118', 'YOGITH_KRISHNA', 'KAILASHJSONI', 'AARONGILLXX', 'JOSHUA_NIGEL_MENEZES', 'PARSH1', 'KNOW_TARUN', 'NIMIECHANDHOK', '3SHARAIZADA', 'SIDDHI_BHANDARI', 'PRADDY_12', 'ADITYA_GARG114', 'THIRTEENTH_COMMAND_1', '2407ALINA', 'DEEPAKBAJI', '_MJH18', 'HEMANTH__KR', 'MAHASHRAFALI', 'GUPTA16HARSH', 'EDEN_EVA_PAUL', 'AEZAZADEEB', 'NEHABAVEJAA', 'ZARA_SHAFEEQ', 'EKTAINITIATIVE', 'KALINDI1122', 'REMINISCE_EVENTS_CO', 'AVASURI001', 'SACHINMJOHN', 'GODLY_97', 'HARSHAL_HKN', 'SA.CHINKUMAR8927', 'VP_VENKS', 'AARON10ALB', 'NYLA_SRINIVASAN', 'AVANIKA_L', 'YASMINOBRIEN', '_.MANAV27', 'BHAKTIPARMAR_03', 'HARDIKASHRIYA', 'BIPANSHU.SHARMA', 'HENA.MISTRY', 'JAYCHOPS', 'SARTHAK_VARMA03', 'NISHANT_1901', 'KRISHANGUPTA_', 'ANCHITSHETHIA', 'DIA_JHAVERI', 'NANDHA_KUMAARAN.K', 'DHIYA.VIPUL', 'VINS0UP', 'KUSH12KUSH', 'SIDKHEMKA', 'NINAPA_X', 'KAUSHAL._.MANIYAR', 'RAGAN_JAIN', 'DEANNAKOTECHA', 'ENIG.MAT.IC', 'MAHIKAXGUPTA', 'PRITIKA_LALALALA', 'JAHNAVITHAKAR', 'SIMPLY_SATYA_', 'ASTH.A', 'EMAN_FAREEED', 'IISHAPONKSHE', 'KR1SHAN__', '_VRINDA.R_', 'NEHA._209', 'SONALIHAZAREESING', 'KRISHA_AGARWAL', 'AARAV.PANDIAN3', 'MALLIKAARYA', 'DHIRAJ_B213', 'ARAVIND_MAMA', 'KASHVIIIIII', 'ARUN.SHARMA1', 'SANAGOGIA', 'TEMPTASIANSDJS', 'VIREN.H_', 'JAYENEVENTSPR', '_TEJAYSINGH', 'NOVALIDANSWERS', 'PRARTHIT_SANGHOI', 'KABIR_BATRA', 'PRATHIT07', 'SAKETH_U', 'KAURD28', 'HARSHATOMY', 'PRERNACHOKHANY', 'ANUDEEP_ETERNAL7', 'DIXITBHALANI', 'SENJUTISENGUPTA_', 'VAIDEHIJAJU', 'DJKRISH_.OFFICIAL', 'KAUR_BAGGA', '_SNEHAAAA_X', 'AAYUSHK_5', 'SANDISI.GUNASEKARA', 'KARANVEERNATH19', 'DHANANJAYAN_RAMASAMI', '_A_N_Y_A_V_I_R_D_I_', 'NISHKALABALAJI', 'CHAYABHOJWANI', 'HEY_ITS_ANISH', 'ALLANTECHBOII', 'SURYACHORDIA20', 'VATSALGOEL2501', 'ARAISH24', 'THEINDIANSNEXTDOOR', 'SUHANASATIJA', 'TGEE_20', 'ADDITEE_GUPTA', 'AIMEED02', 'ANANDSK98', 'VANSHIKADUTT', 'MDHV99']
# disclaimer: this is some of the worst code i have ever written


TARGET_ACCOUNT = "thasbath"
class nrIG:
    def __init__(self):
        self.TIMEOUT_DURATION  = 3
        self.IGURL = 'https://www.instagram.com/'
        edge_options = EdgeOptions()
        edge_options.use_chromium = True

        user_data_dir = r"C:\Users\jasbi\AppData\Local\Microsoft\Edge\User Data\Selenium Dev"
        edge_options.add_argument("user-data-dir={}".format(user_data_dir)); 

        edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        driver_location = r"D:\FILES\Desktop\other\IGTools\msedgedriver.exe"


        self.browser = Edge(executable_path=driver_location, options=edge_options)

        self.browser.get(self.IGURL)

        self.FOLLOW_BUFFER_DURATION = 30



    def ScrollPopupBoxNew(self, pop_up_box, target_element_selector):
        num_elements_found_old = -1
        num_elements_found = 0

        ActionChains(self.browser).move_to_element(pop_up_box).click().send_keys(Keys.PAGE_DOWN).perform()
        sleep(3)
        ActionChains(self.browser).move_to_element(pop_up_box).click().perform()

        found_ig_accounts = []


        while num_elements_found_old != num_elements_found and RUNNING:
   
            for i in range(0,5):
                ActionChains(self.browser).move_to_element(pop_up_box).send_keys(Keys.PAGE_DOWN).perform()
                sleep(1)
            tmp = num_elements_found

            users_found = self.browser.find_elements(by=By.CSS_SELECTOR, value=target_element_selector)
            num_elements_found = len(users_found)
            num_elements_found_old = tmp


            start_index = num_elements_found_old - 1
            if start_index < 0: start_index = 0
            end_index = num_elements_found - 1
            
            found_ig_accounts_tmp = users_found[start_index: end_index]

            for found_ig_account in found_ig_accounts_tmp:
                if not RUNNING: break
                try:
                    account_text = found_ig_account.text.upper().split("\n")
                    user_name = account_text[0]
                    
                    following_status = account_text[-1]
                    print("FOUND USER {} : {}".format(user_name, following_status))
                    if following_status != "FOLLOW":
                        continue
                    if user_name in REQUESTS_SENT:
                        print("SENT ALREADY!")
                        continue

                    follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))
                    follow_button.click()
                    sleep(2)
                    if follow_button.text.upper() == "FOLLOW":
                        print("LIMIT REACHED")
                        continue
                    print("FOLLOWED USER {}".format(user_name))
                    REQUESTS_SENT.append(user_name)

                    for i in range(self.FOLLOW_BUFFER_DURATION):
                        print("SLEEPING {}TH SECOND".format(i))
                        sleep(1)
                except Exception as e:
                    print(e)
                    continue



    def __UnfollowUsers(self, pop_up_box, target_element_selector,user_links):
        num_elements_found_old = -1
        num_elements_found = 0

        ActionChains(self.browser).move_to_element(pop_up_box).click().send_keys(Keys.PAGE_DOWN).perform()
        sleep(3)
        ActionChains(self.browser).move_to_element(pop_up_box).click().perform()

        found_ig_accounts = []


        while num_elements_found_old != num_elements_found:
   
            for i in range(0,5):
                ActionChains(self.browser).move_to_element(pop_up_box).send_keys(Keys.PAGE_DOWN).perform()
                sleep(1)
            tmp = num_elements_found

            users_found = self.browser.find_elements(by=By.CSS_SELECTOR, value=target_element_selector)
            num_elements_found = len(users_found)
            num_elements_found_old = tmp


            start_index = num_elements_found_old - 1
            if start_index < 0: start_index = 0
            end_index = num_elements_found - 1
            
            found_ig_accounts_tmp = users_found[start_index: end_index]

            # found_ig_accounts_tmp = []
            for found_ig_account in found_ig_accounts_tmp:
                try:
                    account_text = found_ig_account.text.upper().split("\n")
                    user_name = account_text[0]
                    user_link = 'https://www.instagram.com/{}/'.format(user_name.lower())
                    
                    following_status = account_text[-1]
                    print("FOUND USER {} : {}".format(user_name, following_status))
                    follow_button = found_ig_account.find_element(by=By.CSS_SELECTOR, value="div.{}".format("Pkbci button"))

                    if user_link in user_links and following_status == "FOLLOWING":
                        follow_button.click()
                        try:
                            unfollow_button = [button for button in self.browser.find_elements(by=By.TAG_NAME, value='button') if button.text.lower() == "unfollow"][0]
                            unfollow_button.click()
                        except Exception as e:
                            continue
                        sleep(2)

                        if follow_button.text.upper() == "FOLLOW":
                            print("UNFOLLOWED USER {}".format(user_link))
                            REQUESTS_SENT.append(user_name)
                            ActionChains(self.browser).move_to_element(pop_up_box).click().perform()
                            for i in range(30):
                                print("SLEEPING {}TH SECOND".format(i))
                                sleep(1)
                            continue
                        
                        print("LIMIT REACHED")


                except Exception as e:
                    print(e)
                    continue


            

    
    

    
    def ScrollFollowing(self, instagramName):
        self.browser.get(self.IGURL + instagramName)
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a'))).click()
        followersBox =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div._1XyCr')))
        # self.__UnfollowUsers(followersBox, 'div.isgrP ul li', NON_FOLLOWERS)

        self.ScrollPopupBoxNew(followersBox, 'div._1XyCr ul li')
        return [element.get_attribute("href") for element in self.browser.find_elements(by=By.CSS_SELECTOR, value="a.notranslate._0imsa")]


    def ScrollFollowers(self, instagramName):
        self.browser.get(self.IGURL + instagramName)
        WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'))).click()
        followersBox =  WebDriverWait(self.browser, self.TIMEOUT_DURATION).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.isgrP')))
        self.ScrollPopupBoxNew(followersBox, 'div.isgrP ul li')
        # self.__UnfollowUsers(followersBox, 'div.isgrP ul li', NON_FOLLOWERS)
        return [element.get_attribute("href") for element in self.browser.find_elements(by=By.CSS_SELECTOR, value="a.notranslate._0imsa")]

    
    def GetListOfThoseWhoDontFollow(self,instagramName):

        try:
            
            # followers_names = [follower.lower() for follower in self.ScrollFollowers(instagramName)]
            # following_names = [following.lower() for following in self.ScrollFollowing(instagramName)]
            # res = []

            # for following_account in following_names:
            #     if following_account in followers_names: continue
            #     res.append(following_account)
            self.ScrollFollowing(instagramName)
        except Exception as e:
            print(e)
    def UnfollowThoseWhoDontFollow(self, instagramName, list_of_non_followers): 
        self.ScrollFollowing(instagramName)

        pass
        

IGBot = nrIG()
   




def SaveChanges():
    f = open("requests_sent.txt", "w")
    f.write(str(REQUESTS_SENT))
    f.close()

    print("SAVED CHANGES!")


def ListenForCommands():
    while True:
        command = input("ENTER COMMAND:")
        if command.upper() == "SAVE":
            SaveChanges()
            print("SAVED CHANGES")
        
        if command.upper() == "EXIT":
            global RUNNING
            RUNNING = False
            SaveChanges()
            print("EXITING APPLICATION")




atexit.register(SaveChanges)
            




def Farm():
    # DONE_ACCOUNTS = ["bathindiandancesociety","bathindiansoc", "bathtamilsoc"]


    listener_thread = threading.Thread(target=ListenForCommands)
    listener_thread.setDaemon(True)
    listener_thread.start()

    TARGET_ACCOUNTS = ["thesubath"]
    # TARGET_ACCOUNTS = ["bathindiandancesociety","bathindiansoc", "bathtamilsoc", "bathhindusoc", "bathmalayaleesoc", "thesubath"]


    for target_account in TARGET_ACCOUNTS:
        print("INITIATING {}".format(target_account))
        try:
            # IGBot.GetListOfThoseWhoDontFollow("thesubath")
            # i=3
            followers_list = IGBot.ScrollFollowers(target_account)
            # following_list = IGBot.ScrollFollowing(target_account)

        except Exception as e:
            print(e)
        print("DONE_{}".format(target_account))



    

# Follow()






try:
    REQUESTS_SENT = eval(open("requests_sent.txt", "r").read())
    Farm()

except Exception as e:
    f = open("requests_sent.txt", "w")
    f.write(str(REQUESTS_SENT))
    f.close()








