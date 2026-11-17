# にじのくに 第1話：制作・費用・動画生成実行計画 v1
更新 2026-11-17

## 検証した料金と重要な制約
- Runway Standard: 月払い $15 / 625 credits
- Runway Pro: 月払い $35 / 2250 credits
- Runway Max: 月払い $95 / 9500 credits
- Gen-4.5 は 12 credits/sec。Pro 2250 credits で理論上187.5秒。
- Gen-4 Turbo は Pro で理論上375秒（公式の換算値）。
- Runway Unlimitedは2026-06-01に新規受付終了。既存契約者の移行予定日は2026-11-30。
- Kling公式は会員ランク別クレジット制。具体的な現行価格は契約画面で要確認。
- 上記は再生成なしの理論値。失敗カットを考慮する。

出典:
https://runway.com/ja/pricing
https://help.runwayml.com/hc/en-us/articles/52068047744019-Unlimited-plan-is-switching-to-Max
https://kling.ai/docs/payment-policy

## 方針
- 初回は課金しない。主人公ラビの画像参照を使い5秒の「手を振る」カットで品質を検証。
- 合格後、約160秒の第1話を、動画生成する重要カットと、編集・カメラ演出・音声で成立するカットに分解。
- 日本語・英語は同じ映像を使い音声のみ差し替える。
- 人間の承認なしに課金や公開を行わない。
- Google Driveは素材の正本保管先、GitHubは台本・プロンプト・自動化コード。

## キャラクター固定条件
ラビ: 白いふわふわの毛、ピンクの長耳、大きな茶色の目、淡い青の花刺繍ワンピース、茶色の小さなリュック。耳・顔・衣装・体格を全ショットで一致させる。既存設定画をimage referenceに使う。

## 動画生成用プロンプト 01: 手を振る 5秒
Input: single reference image of Labi character, preferably a clean full-body crop from the character sheet.
Prompt (EN):
A polished 3D animated children's film shot. The same fluffy white bunny girl from the reference, with pink inner ears, large brown eyes, pale blue floral dress and small brown backpack, stands in a sunny magical meadow under a rainbow. She smiles warmly at the camera, raises her right paw and waves gently twice, with natural ear bounce, subtle blinking and soft fur motion. The camera makes a very slow smooth dolly-in. Consistent face, exact outfit, stable anatomy, clean animation, warm daylight, vivid but soft colors, 16:9, five seconds. No text, no extra limbs, no morphing, no character changes, no cuts.
Negative: identity drift, outfit change, extra paws, deformed fingers, flicker, rapid motion, camera shake, duplicate character, watermark, text.

## 動画生成用プロンプト 02: 驚く 5秒
The same fluffy white bunny girl in the pale blue floral dress and brown backpack stands in Rainbow Land. Behind her, a luminous rainbow gently fades away. She looks upward, blinks, then opens her eyes wide in surprise and takes one small step backward. Gentle cinematic camera push, consistent face and costume, child-friendly emotional expression, stable 3D animation, five seconds, 16:9. No cuts, no text, no morphing.

## 動画生成用プロンプト 03: 旅立ち 5秒
The same fluffy white bunny girl with pale blue floral dress and brown backpack stands at a sunny forest path. She takes a breath, smiles with quiet determination, turns and walks three small steps toward the magical forest. The camera follows slowly from behind at child eye level. Gentle ear bounce, stable outfit and body proportions, five seconds, 16:9. No cuts, no text, no morphing.

## 第1話全11カット・実行優先順位
01 0:00–0:12 世界紹介: 背景画像+ゆっくりカメラ移動
02 0:12–0:24 住まい紹介: 背景+カメラ移動
03 0:24–0:38 ラビ紹介: 5秒動画生成+ナレーション/編集
04 0:38–0:52 ベア紹介: キャラ参照確定後5秒動画
05 0:52–1:06 フォックス紹介: キャラ参照確定後5秒動画
06 1:06–1:20 リリー紹介: キャラ参照確定後5秒動画
07 1:20–1:38 虹のそばで遊ぶ: 複数キャラ同時生成を試験
08 1:38–1:50 虹が消える: 5秒の重要演出動画
09 1:50–2:10 相談会: 口パクなし、ナレーション主体、リアクションカット
10 2:10–2:25 ラビの決意: 5秒動画
11 2:25–2:40 旅立ち: 5秒動画

## 品質ゲート
1. 同じラビに見えるか
2. 手・耳・衣装が変形しないか
3. 5秒の動きが自然か
4. 子どもが怖がらないか
5. 商用利用規約・ウォーターマーク条件を満たすか
6. 生成費用が見積内か

## 状態
計画とプロンプトのみ。外部動画生成は未実行。新規課金なし。Google Driveへの新規動画アップロードなし。
