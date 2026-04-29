# 🎮 Minecraft Action Framework

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Minecraft](https://img.shields.io/badge/minecraft-1.21.4-green)
![License](https://img.shields.io/badge/license-MIT-orange)

Advanced action management system for Minecraft 1.21.4 datapacks.

## ✨ Özellikler

- 🎯 **Action Queue System** - Eylemlerinizi sıraya koyun ve otomatik işleyin
- 🔗 **Chain Actions** - Birden fazla eylemi zincirleme olarak çalıştırın
- ⏱️ **Timer System** - Zamanlı eylemler oluşturun
- 🎵 **Sound & Particle Management** - Ses ve parçacık efektlerini kolayca yönetin
- 📝 **Macro Support** - Parametreli fonksiyonlar ile dinamik komutlar
- 🐛 **Debug Mode** - Gelişmiş hata ayıklama araçları
- 📊 **Performance Optimized** - Verimli tick işleme
- 📚 **Rich API** - Kolay entegrasyon için kapsamlı API

## 📦 Kurulum

1. Release sayfasından en son versiyonu indirin
2. Datapack'i `.minecraft/saves/[World Name]/datapacks/` klasörüne kopyalayın
3. Oyuna girin ve `/reload` komutunu çalıştırın
4. Framework otomatik olarak yüklenecektir

## 🚀 Hızlı Başlangıç

### Basit Kullanım

```mcfunction
# Bir mesaj gönder
data modify storage action_framework:temp api_input set value {\
    type:"message",\
    target:"@a",\
    message:'{"text":"Hello World!","color":"gold"}'\
}
function action_framework:api/add_action
```

### Chain Action

```mcfunction
# Zincirleme eylemler
function action_framework:examples/chain_example
```

### Macro Kullanımı

```mcfunction
# Oyuncuya eşya ver
function action_framework:macros/give_item {\
    target:"@s",\
    item:"minecraft:diamond",\
    count:"5"\
}
```

## 📖 Dokümantasyon

- [Kullanım Kılavuzu](docs/USAGE.md) - Detaylı kullanım talimatları
- [API Referansı](docs/API.md) - Fonksiyon ve veri yapıları
- [Örnekler](docs/EXAMPLES.md) - Kod örnekleri

## 🎯 Action Türleri

| Tür | Açıklama |
|-----|----------|
| `command` | Minecraft komutu çalıştır |
| `message` | Oyunculara mesaj gönder |
| `sound` | Ses efekti çal |
| `particle` | Parçacık efekti oluştur |
| `summon` | Entity spawn et |
| `chain` | Zincirleme eylemler |
| `delay` | Geciktirilmiş eylem |
| `conditional` | Koşullu eylem |

## 🛠️ API Fonksiyonları

```mcfunction
# Bilgi görüntüle
function action_framework:api/info

# Debug modu
function action_framework:api/debug_toggle

# Kuyruğu temizle
function action_framework:api/clear_queue

# Yardım menüsü
function action_framework:api/help
```

## 🧪 Örnekler

Framework, kullanımı göstermek için birçok örnek içerir:

```mcfunction
# Basit örnek
function action_framework:examples/basic

# Boss tanıtımı
function action_framework:examples/boss_intro

# Minigame başlangıcı
function action_framework:examples/minigame_start
```

## ⚙️ Konfigürasyon

```mcfunction
# Debug modu aç
data modify storage action_framework:main config.debug set value 1b

# Maximum queue boyutu ayarla
data modify storage action_framework:main config.max_queue_size set value 200

# Action logging kapat
data modify storage action_framework:main config.log_actions set value 0b
```

## 🔧 Geliştirme

### Gereksinimler
- Python 3.8+
- Minecraft 1.21.4

### Build

```bash
python build.py
```

### Test

```bash
python -m pytest tests/
```

## 📊 Performans

- ✅ Minimal tick impact
- ✅ Efficient queue processing
- ✅ Optimized storage operations
- ✅ Smart caching system

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Changelog

Detaylı değişiklikler için [CHANGELOG.md](CHANGELOG.md) dosyasına bakın.

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👥 Yazarlar

- **asn44nb** - *Initial work* - [GitHub](https://github.com/asn44nb)
- **RunToolkit Team** - [Organization](https://github.com/runtoolkit)

## 🙏 Teşekkürler

- Minecraft community
- Datapack creators
- Contributors

## 🔗 Bağlantılar

- [GitHub Repository](https://github.com/runtoolkit/minecraft-action-framework)
- [Issue Tracker](https://github.com/runtoolkit/minecraft-action-framework/issues)
- [Discussions](https://github.com/runtoolkit/minecraft-action-framework/discussions)

## 📞 İletişim

Sorularınız için:
- GitHub Issues açın
- Discussions kullanın
- asn44nb @ GitHub

---

<div align="center">

**Made with ❤️ by RunToolkit**

[⭐ Star](https://github.com/runtoolkit/minecraft-action-framework) · [🐛 Report Bug](https://github.com/runtoolkit/minecraft-action-framework/issues) · [💡 Request Feature](https://github.com/runtoolkit/minecraft-action-framework/issues)

</div>
