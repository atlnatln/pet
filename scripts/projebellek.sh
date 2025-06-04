#!/bin/bash
# filepath: scripts/projebellek.sh

# ProjeBellek için klasörler oluştur
mkdir -p .github/projebellek/entries

# Ana fonksiyon
pb_main() {
  case "$1" in
    pb-add)
      shift
      pb_add "$@"
      ;;
    pb-query)
      shift
      pb_query "$@"
      ;;
    *)
      echo "Kullanım: pb-add <başlık> <içerik> <etiketler> [<tür>] [<durum>] veya pb-query <sorgu>"
      ;;
  esac
}

# Bilgi kaydetme fonksiyonu
pb_add() {
  if [ $# -lt 3 ]; then
    echo "Eksik parametreler. Kullanım: pb-add <başlık> <içerik> <etiketler> [<tür>] [<durum>]"
    return 1
  fi

  TITLE="$1"
  CONTENT="$2"
  TAGS="$3"
  TYPE="${4:-karar}"
  STATUS="${5:-aktif}"
  
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  ID="pb_${TYPE:0:3}_v1_${TIMESTAMP}"
  
  # JSON dosyası oluştur
  cat > ".github/projebellek/entries/${ID}.json" <<EOF
{
  "id": "${ID}",
  "title": "${TITLE}",
  "content": "${CONTENT}",
  "tags": [$(echo $TAGS | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')],
  "type": "${TYPE}",
  "status": "${STATUS}",
  "created_at": "$(date -Iseconds)",
  "updated_at": "$(date -Iseconds)",
  "author": "$(whoami)",
  "version": 1,
  "related_records": [],
  "scope": "",
  "expires_at": null
}
EOF

  # Index'e ekle
  if [ ! -f ".github/projebellek/index.json" ]; then
    echo '{"entries":[]}' > ".github/projebellek/index.json"
  fi
  
  # jq ile indexe ekle (jq kurulu olmalıdır)
  if command -v jq &> /dev/null; then
    jq --arg id "$ID" --arg title "$TITLE" --arg tags "$TAGS" \
      '.entries += [{"id": $id, "title": $title, "tags": $tags|split(","), "updated_at": "'$(date -Iseconds)'"}]' \
      .github/projebellek/index.json > .github/projebellek/index.json.tmp && \
      mv .github/projebellek/index.json.tmp .github/projebellek/index.json
  else
    echo "⚠️ jq komutu bulunamadı. Index güncellenemedi."
  fi
  
  echo "✅ Kayıt eklendi: $ID"
}

# Bilgi arama fonksiyonu
pb_query() {
  if [ $# -lt 1 ]; then
    echo "Eksik parametre. Kullanım: pb-query <sorgu>"
    return 1
  fi
  
  QUERY="$1"
  
  if [[ "$QUERY" == id:* ]]; then
    # ID ile ara
    ID="${QUERY#id:}"
    if [ -f ".github/projebellek/entries/${ID}.json" ]; then
      echo "📄 Bulunan kayıt (ID: $ID):"
      cat ".github/projebellek/entries/${ID}.json" | jq '.'
    else
      echo "❌ Kayıt bulunamadı: $ID"
    fi
  elif [[ "$QUERY" == etiket:* ]]; then
    # Etiket ile ara
    TAG="${QUERY#etiket:}"
    grep -l "\"$TAG\"" .github/projebellek/entries/*.json | while read file; do
      echo "📄 $(basename "$file" .json):"
      cat "$file" | jq '.title + " - " + .content[0:50] + "..."'
    done
  else
    # Genel arama
    grep -l "$QUERY" .github/projebellek/entries/*.json | while read file; do
      echo "📄 $(basename "$file" .json):"
      cat "$file" | jq '.title + " - " + .content[0:50] + "..."'
    done
  fi
}

# Ana işlevi çağır
pb_main "$@"