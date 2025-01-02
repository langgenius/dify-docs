# با ابزارهای API با Cloudflare Workers  مستقر شوید

## شروع

از آنجا که Dify API Extension به یک آدرس اینترنتی عمومی به عنوان API Endpoint  نیاز دارد، باید API Extension  خود را در یک آدرس اینترنتی عمومی  مستقر کنیم.  در اینجا،  ما از Cloudflare Workers برای استقرار API Extension  خود استفاده می‌کنیم.

ما [Example GitHub Repository](https://github.com/crazywoola/dify-extension-workers)  را کپی می‌کنیم، که شامل یک API Extension  ساده است.  ما می‌توانیم آن را به عنوان یک پایه تغییر دهیم.

```bash
git clone https://github.com/crazywoola/dify-extension-workers.git
cp wrangler.toml.example wrangler.toml
```

فایل `wrangler.toml`  را باز کنید و `name`  و `compatibility_date`  را به نام برنامه  و تاریخ سازگاری  خود تغییر دهید.

یک پیکربندی مهم در اینجا `TOKEN`  در `vars`  است که هنگام افزودن API Extension  در Dify  باید آن را ارائه دهید.  به دلایل امنیتی،  استفاده از یک رشته تصادفی به عنوان Token  توصیه می‌شود.  شما نباید Token  را به طور مستقیم در کد منبع بنویسید،  بلکه آن را از طریق متغیرهای محیطی منتقل کنید.  بنابراین،  wrangler.toml  خود را در مخزن کد خود متعهد نکنید.

```toml
name = "dify-extension-example"
compatibility_date = "2023-01-01"

[vars]
TOKEN = "bananaiscool"
```

این API Extension  یک نقل قول تصادفی از Breaking Bad  را برمی‌گرداند.  می‌توانید منطق این API Extension  را در `src/index.ts`  تغییر دهید.  این مثال نحوه تعامل با یک API  شخص ثالث را نشان می‌دهد.

```typescript
// ⬇️ منطق خود را در اینجا پیاده سازی کنید ⬇️
// point === "app.external_data_tool.query"
// https://api.breakingbadquotes.xyz/v1/quotes
const count = params?.inputs?.count ?? 1;
const url = `https://api.breakingbadquotes.xyz/v1/quotes/${count}`;
const result = await fetch(url).then(res => res.text())
// ⬆️ منطق خود را در اینجا پیاده سازی کنید ⬆️
```

این مخزن همه تنظیمات به جز منطق تجاری  را ساده می‌کند.  می‌توانید به طور مستقیم از دستورات `npm`  برای استقرار API Extension  خود استفاده کنید.

```bash
npm run deploy
```

پس از استقرار موفقیت‌آمیز،  یک آدرس اینترنتی عمومی دریافت خواهید کرد که می‌توانید آن را در Dify  به عنوان یک API Endpoint  اضافه کنید.  لطفاً توجه داشته باشید که مسیر `endpoint`  را از دست ندهید.

<figure><img src="../../../.gitbook/assets/api_extension_edit (1).png" alt=""><figcaption><p>افزودن API Endpoint  در Dify</p></figcaption></figure>

<figure><img src="../../../.gitbook/assets/app_tools_edit (1).png" alt=""><figcaption><p>افزودن API Tool  در صفحه ویرایش برنامه</p></figcaption></figure>

## سایر منطق TL;DR

### درباره Bearer Auth

```typescript
import { bearerAuth } from "hono/bearer-auth";

(c, next) => {
    const auth = bearerAuth({ token: c.env.TOKEN });
    return auth(c, next);
},
```

منطق احراز هویت Bearer  ما به شرح بالا است.  ما از بسته `hono/bearer-auth`  برای احراز هویت Bearer  استفاده می‌کنیم.  می‌توانید از `c.env.TOKEN`  در `src/index.ts`  برای دریافت Token  استفاده کنید.

### درباره اعتبارسنجی پارامتر

```typescript
import { z } from "zod";
import { zValidator } from "@hono/zod-validator";

const schema = z.object({
  point: z.union([
    z.literal("ping"),
    z.literal("app.external_data_tool.query"),
  ]), // 'point'  را به دو مقدار خاص محدود می‌کند
  params: z
    .object({
      app_id: z.string().optional(),
      tool_variable: z.string().optional(),
      inputs: z.record(z.any()).optional(),
      query: z.any().optional(),  // string or null
    })
    .optional(),
});
```

ما از `zod`  برای تعریف انواع پارامترها استفاده می‌کنیم.  می‌توانید از `zValidator`  در `src/index.ts`  برای اعتبارسنجی پارامترها استفاده کنید.  پارامترهای معتبر را از طریق `const { point, params } = c.req.valid("json");`  دریافت کنید.  `point`  ما فقط دو مقدار دارد،  بنابراین از `z.union`  برای تعریف استفاده می‌کنیم.  `params`  یک پارامتر اختیاری است که با `z.optional`  تعریف شده است.  این پارامتر شامل یک پارامتر `inputs`  است،  یک نوع `Record<string, any>`  که یک شی با کلیدهای رشته‌ای و هر نوع  ارزش را نشان می‌دهد.  این نوع می‌تواند هر نوع شی را نشان دهد.  می‌توانید پارامتر `count`  را در `src/index.ts`  با استفاده از `params?.inputs?.count`  دریافت کنید.

### دسترسی به  Log  های  Cloudflare Workers

```bash
wrangler tail
```

## محتوای مرجع

* [Cloudflare Workers](https://workers.cloudflare.com/)
* [Cloudflare Workers CLI](https://developers.cloudflare.com/workers/cli-wrangler/install-update)
* [Example GitHub Repository](https://github.com/crazywoola/dify-extension-workers)


