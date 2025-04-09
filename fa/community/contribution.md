# مشارکت

پس شما به دنبال مشارکت در Dify هستید - عالی است، ما مشتاقانه منتظر دیدن کارهای شما هستیم. به عنوان یک استارتاپ با تعداد کارکنان و بودجه محدود، ما آرزوی بزرگی داریم که  intuitive ترین گردش کار را برای ساخت و مدیریت برنامه های LLM طراحی کنیم. هر کمکی از طرف جامعه، واقعا ارزشمند است.

با توجه به موقعیت کنونی ما، باید چابک و سریع عمل کنیم، اما همچنین می خواهیم اطمینان حاصل کنیم که مشارکت کنندگانی مانند شما، به آسانی و بدون هیچ مشکلی  در این فرآیند سهیم شوند. به همین منظور این راهنمای مشارکت را گردآوری کرده ایم، که هدف آن آشنایی شما با کد پایه و نحوه کار ما با مشارکت کنندگان است، تا بتوانید به سرعت به بخش سرگرم کننده آن بپرید.

این راهنما، مانند Dify، به طور مداوم در حال پیشرفت است. اگر گاهی اوقات با پروژه واقعی همگام نباشد، قدردانی ما از درک شما را به همراه دارد، و هرگونه بازخوردی برای بهبود آن از شما استقبال می شود.

در مورد مجوز، لطفاً چند لحظه وقت بگذارید و [مجوز و توافق نامه مشارکت](https://github.com/langgenius/dify/blob/main/LICENSE) ما را بخوانید. جامعه نیز  [قوانین رفتاری](https://github.com/langgenius/.github/blob/main/CODE_OF_CONDUCT.md) را رعایت می کند.

### قبل از شروع

[پیدا کردن](https://github.com/langgenius/dify/issues?q=is:issue+is:closed) یک موضوع موجود، یا [باز کردن](https://github.com/langgenius/dify/issues/new/choose)  موضوع جدید.  ما موضوعات را به دو نوع دسته بندی می کنیم:

#### درخواست ویژگی:

* اگر یک درخواست ویژگی جدید را باز می کنید، می خواهیم توضیح دهید که ویژگی پیشنهادی چه چیزی را انجام می دهد و تا حد امکان اطلاعات زمینه را  درج کنید.  [@perzeusss](https://github.com/perzeuss)  یک [Copilot  درخواست ویژگی](https://udify.app/chat/MK2kVSnw1gakVwMX)  مطمئن را ساخته است که به شما در  draft کردن  نیازهایتان  کمک می کند.  مایلید امتحان کنید.
* اگر می خواهید یکی از موضوعات موجود را انتخاب کنید،  simply یک نظر  در زیر آن  بگذارید و  این را بگویید.

    یک عضو تیم که در جهت مرتبط کار می کند،  informed خواهد شد.  اگر همه چیز خوب به نظر می رسد، آنها  به شما اجازه شروع  coding را  خواهند داد. از شما می خواهیم که تا آن زمان  از  کار روی  feature  خودداری کنید،  تا هیچ کاری شما هدر نرود اگر  تغییراتی را پیشنهاد دهیم.

    بسته به اینکه  feature  پیشنهادی  در کدام  area قرار دارد،  ممکن است با اعضای مختلف  تیم  صحبت کنید.  در اینجا خلاصه  area های  که هر عضو  تیم  در حال حاضر  روی آن  کار می کند  آورده شده است:

    | عضو                                                                                  |  scope                                                |
    | --------------------------------------------------------------------------------------- | ---------------------------------------------------- |
    | [@yeuoly](https://github.com/Yeuoly)                                                    | طراحی Agents                                  |
    | [@jyong](https://github.com/JohnJyong)                                                  | طراحی خط لوله  RAG                                  |
    | [@GarfieldDai](https://github.com/GarfieldDai)                                          |  ساخت گردش کار  orchestration ها                     |
    | [@iamjoel](https://github.com/iamjoel) & [@zxhlyh](https://github.com/zxhlyh)           | آسان کردن استفاده از Frontend                       |
    | [@guchenhe](https://github.com/guchenhe) & [@crazywoola](https://github.com/crazywoola) | تجربه  developer  و  نقاط تماس برای هر  چیزی |
    | [@takatost](https://github.com/takatost)                                                |  جهت کلی  product  و  architecture           |

    نحوه اولویت بندی ما:

    | نوع ویژگی                                                 |  priority        |
    | ------------------------------------------------------------ | --------------- |
    |  ویژگی های  priority بالا که توسط یک عضو تیم برچسب گذاری شده اند    |  priority بالا   |
    |  درخواست های ویژگی محبوب  از [تخته  feedback  جامعه](https://github.com/langgenius/dify/discussions/categories/ideas) |  priority متوسط |
    |   ویژگی های  non-core  و  enhancement های جزئی                      |  priority پایین    |
    |  ارزشمند اما  immediate  نیست                                   |   Feature  آینده ای  |

#### هر چیز دیگری (به عنوان مثال گزارش باگ، بهینه سازی عملکرد، تصحیح  typo ):

*   مستقیماً  coding  را شروع کنید.

    نحوه اولویت بندی ما:

    | نوع  Issue                                                                          |  priority        |
    | ----------------------------------------------------------------------------------- | --------------- |
    | باگ ها در  function های  core  (عدم امکان ورود، عدم  function کردن  برنامه ها،  loopholes  امنیتی) |   Critical        |
    |  باگ های  non-critical  ،  boost های  performance                                               |  priority متوسط |
    |  رفع  minor  (  typos  ،   UI  confusing   اما  working  )                                       |  priority پایین    |

### نصب

در اینجا  steps  برای  setup کردن  Dify  برای  development  آورده شده است:

#### 1.  fork  این  repository 

#### 2.  clone  repo

repo  fork شده را  از  terminal  خود  clone  کنید:

```
git clone git@github.com:<github_username>/dify.git
```

#### 3.  verify  dependencies

Dify   به  dependencies  زیر برای  build  نیاز دارد، مطمئن شوید  که  آن ها  بر روی  سیستم شما نصب شده اند:

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Node.js v18.x (LTS)](http://nodejs.org)
* [npm](https://www.npmjs.com/) نسخه 8.x.x یا  [Yarn](https://yarnpkg.com/)
* [Python](https://www.python.org/) نسخه 3.10.x

#### 4.  installations

Dify  از  backend  و  frontend  تشکیل شده است. با `cd api/` به  directory  backend   رفته، سپس [README  backend](https://github.com/langgenius/dify/blob/main/api/README.md) را دنبال کنید تا آن را نصب کنید. در یک  terminal  مجزا، با  `cd web/`  به  directory  frontend  رفته، سپس  [README  frontend](https://github.com/langgenius/dify/blob/main/web/README.md) را دنبال کنید تا نصب شود.

[FAQ  نصب](https://docs.dify.ai/learn-more/faq/install-faq) را  check  کنید  تا لیستی از  issues  رایج و  steps  برای  troubleshoot  آن ها را مشاهده کنید.

#### 5.  visit  dify  در  browser  خود

برای  validate  کردن  setup  خود، به  [http://localhost:3000](http://localhost:3000) (  default  ، یا  URL  و  port  خودتان) در  browser  خود  سر بزنید.  اکنون باید  Dify  را   up and running  ببینید.

###  Developing

اگر  provider  مدل  اضافه می کنید، [این  guide](https://github.com/langgenius/dify/blob/main/api/core/model_runtime/README.md)   برای  شما  است.

اگر  tools  استفاده شده در Agent Assistants  و  Workflows  را  اضافه می کنید،  [این  guide](https://github.com/langgenius/dify/blob/main/api/core/tools/README.md)   برای  شما  است.

> **Note** : اگر  می خواهید  به  tool  جدیدی  مشارکت کنید،  مطمئن شوید که  اطلاعات  تماس خود را  در  فایل 'YAML'  tool  درج کرده  اید  و  PR  docs  مربوطه را  در  repository   [Dify-docs](https://github.com/langgenius/dify-docs/tree/main/en/guides/tools/tool-configuration)  submit  کرده  اید.

برای  کمک به شما در  navigate  سریع به  جایی که  مشارکت  شما   fit  می شود،  یک  outline  مختصر و  annotated  از  backend  و  frontend  Dify  به شرح  زیر  است:

#### Backend

backend   Dify   با   [Flask](https://flask.palletsprojects.com/en/3.0.x/)  نوشته شده  و  از  Python  استفاده می  کند.  از   [SQLAlchemy](https://www.sqlalchemy.org/)   برای  ORM  و  [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)   برای  task queueing  استفاده می  کند.  logic   Authorization   از   Flask-login   می گذرد.

```
[api/]
├── constants             //  تنظیمات  ثابت  که در  کل  کد  استفاده  می شود.
├── controllers           //  تعریف  مسیر  API  و  logic   request  handling.           
├── core                  //  orchestration   core   application ،  integraسیون  model   و  tools.
├── docker                //  تنظیمات  مربوط  به  Docker   و  containerization.
├── events                //  event  handling  و  processing
├── extensions            //  extensions  با  framework/platform های  third-party.
├── fields                //  تعریف  field  برای  serialization/marshalling.
├── libs                  //  library  های  قابل  استفاده  مجدد  و  helpers.
├── migrations            //  script  های  مهاجرت  database.
├── models                //  مدل  های  database  و  تعریف  schema.
├── services              //  specify  logic   business.
├── storage               //  storage   کلید  خصوصی.      
├── tasks                 //  handling  وظایف  async  و  background  jobs.
└── tests
```

#### Frontend

وب سایت   بر  روی  [Next.js](https://nextjs.org/)   boilerplate  در  Typescript   bootstrapped   شده  است  و  از   [Tailwind CSS](https://tailwindcss.com/)   برای  styling   استفاده می  کند.   [React-i18next](https://react.i18next.com/)   برای  internationalization  استفاده  می شود.

```
[web/]
├── app                   //  layouts ،  pages  و  components
│   ├── (commonLayout)    //  layout  مشترک  که در  کل  app  استفاده  می شود
│   ├── (shareLayout)     //  layouts  که  به طور  خاص  در  جلسات  token-specific   مشترک  هستند 
│   ├── activate          //  صفحه  activate
│   ├── components        //  shared   by  pages  و  layouts
│   ├── install           //  صفحه  install
│   ├── signin            //  صفحه  signin
│   └── styles            //  style  های  shared  global
├── assets                //  assets  استاتیک
├── bin                   //  script  هایی  که  در  مرحله  build  اجرا  می شوند
├── config                //  تنظیمات  و  option  های  قابل  تنظیم 
├── context               //  context  های  مشترک  که  توسط  بخش های  مختلف  app  استفاده  می شوند
├── dictionaries          //  فایل  های  translate  ویژه  زبان
├── docker                //  تنظیمات  container
├── hooks                 //  hooks  قابل  استفاده  مجدد
├── i18n                  //  تنظیمات  internationalization
├── models                //  شکل  data  models  و  شکل  API  responses  را  توصیف  می کند
├── public                //  meta  assets  مانند  favicon
├── service               //  شکل  action  های  API  را  specify  می کند
├── test                  
├── types                 //  شرح  پارامتر  های  function  و  ارزش  های  return
└── utils                 //  function  های  utility  مشترک
```

###  submit  کردن  PR  خود

در نهایت، زمان  open  کردن  یک  pull request  (PR)  به  repo   ما است.  برای  ویژگی  های  major  ،  اول  آن ها را  به  branch   `deploy/dev`   برای  test  merge   می کنیم،  قبل از  اینکه   به  branch   `main`   بروند.  اگر  با   issues   مانند   merge conflicts   مواجه شدید  یا  نمی دانید  چگونه  یک  pull request  باز کنید،  [آموزش  pull request  GitHub](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)  را  check  کنید.

و تمام!  پس از  merge   شدن  PR   شما،  شما  به عنوان  مشارکت کننده  در  [README](https://github.com/langgenius/dify/blob/main/README.md)   ما  featured  خواهید  شد.

###  getting  help

اگر  در  حین  مشارکت  stuck  شوید  یا  question   burning   داشته  باشید،  simply   queries  خود را  از  طریق   issue  مربوط  GitHub  به  ما  بفرستید،  یا  برای  chat   سریع  به   [Discord](https://discord.gg/AhzKf7dNgk)   بپرید.


