<template>
  <v-container>
    <v-layout
        justify-center
        align-center
        fill-height
    >
      <v-card
          elevation="4"
          width="100%"
          color="secondary"
      >
        <v-card-text
            class="px-8"
            style="line-height: 28px"
            v-html="$store.getters.getSettings.homepage"
        />

        <!--        <v-card-title>-->
        <!--          <v-layout-->
        <!--            justify-center-->
        <!--            align-center-->
        <!--          >-->
        <!--            <v-card-->
        <!--              rounded="lg"-->
        <!--              elevation="6"-->
        <!--            >-->
        <!--        <v-img-->
        <!--            max-width="400px"-->
        <!--            src="/static/img/ans_banner.png"-->
        <!--            :lazy-src="null"-->
        <!--            contain-->
        <!--            position="top"-->
        <!--            class="white&#45;&#45;text"-->
        <!--        />-->
        <!--            </v-card>-->
        <!--          </v-layout>-->
        <!--        </v-card-title>-->
        <!--&lt;!&ndash;        <v-img&ndash;&gt;-->
        <!--&lt;!&ndash;            width="100%"&ndash;&gt;-->
        <!--&lt;!&ndash;            height="100%"&ndash;&gt;-->
        <!--&lt;!&ndash;            src="https://i.imgur.com/uzyctFZ.png"&ndash;&gt;-->
        <!--&lt;!&ndash;            style="position: absolute; opacity: .8"&ndash;&gt;-->
        <!--&lt;!&ndash;            :lazy-src="null"&ndash;&gt;-->
        <!--&lt;!&ndash;            position="top"&ndash;&gt;-->
        <!--&lt;!&ndash;            class="white&#45;&#45;text"&ndash;&gt;-->
        <!--&lt;!&ndash;            gradient="to bottom, rgba(0,0,0,.3), rgba(0,0,0,.3)"&ndash;&gt;-->
        <!--&lt;!&ndash;        >&ndash;&gt;-->

        <!--          <v-card-text class="px-8">-->
        <!--<pre style="white-space: pre-wrap">-->

        <!--<center><b>Vendredi 19 février à 21h00 -> Dimanche 21 février à 01h00</b></center>-->

        <!--<center><b>-= Infos =-</b></center>-->
        <!--&gt; Participation individuelle-->

        <!--&gt; 20 challenges imbriqués, répartis en 5 instances-->
        <!--&gt; Chaque joueur gère ses instances-->
        <!--  > Merci de stopper les instances après les avoir terminées-->
        <!--&gt; Un challenge par utilisateur présent sur la machine (level0, level1...)-->
        <!--&gt; Chaque instance débute avec l'utilisateur <code>level0</code> via ssh-->
        <!--  > Les accès sont disponibles au lancement de l'instance-->
        <!--&gt; Le flag du challenge sert de mot de passe pour se connecter à l'utilisateur suivant-->
        <!--  > Ex : le flag du challenge de l'utilisateur <code>level0</code> sera le mot de passe pour accéder au challenge suivant en se connectant avec l'utilisateur <code>level1</code>-->
        <!--  > Certains flags sont contenu dans un fichier <code>flag</code> à la racine du dossier home de l'utilisateur suivant-->
        <!--&gt; Les flags sont sous la forme ANS{...}-->

        <!--  <center><b>-= Tracks =-</b></center>-->

        <!--&gt; Parcours <b>débutant</b>-->
        <!--    > Initiation aux CTFs-->
        <!--&gt; Parcours <b>confirmé</b>-->
        <!--    > Des lots à la clef pour les 3 premiers à terminer le parcours !-->

        <!--    <center><b>-= Victoire =-</b></center>-->

        <!--&gt; Les <b>3 premiers participants</b> à réussir <b>l'intégralité</b> des challenges du parcours "confirmé" recevrons les lots de leur choix parmi une sélection-->
        <!--&gt; Pour valider sa victoire :-->
        <!--    > Envoi un message à un membre du @Staff sur Discord avec <b>les flags des derniers challenges de chaque instance</b> et <b>ton pseudo sur la plateforme</b>-->
        <!--            > Nous vérifierons que tous les flags ont bien été validé-->
        <!--            > Le timestamp de la dernière soumission validée sera utilisé pour départager deux ex æquo-->

        <!--  <center><b>-= Règles =-</b></center>-->

        <!--&gt; <b>Interdiction</b> d'attaquer l'infra-->
        <!--&gt; Le partage d'information est <b>interdit</b>-->
        <!--&gt; Tous les bruteforces sont à faire sur votre machine (pas sur l'instance)-->
        <!--&gt; Aucun bruteforce <b>sur le réseau</b>-->
        <!--&gt; La publication de solution est <b>interdite</b> jusqu'à la clôture du CTF-->
        <!--&gt; Si le @Staff peut vous dire si le challenge fonctionne comme prévu, il ne pourra confirmer aucune information-->

        <!--En cas de soucis, toute l'équipe est disponible pour répondre à vos questions (@Staff).-->
        <!--      </pre>-->
        <!--          </v-card-text>-->
        <!--        </v-img>-->
      </v-card>
    </v-layout>
  </v-container>
</template>

<script>

export default {
  name: "Home",
  components:{
  },
  data () {
    return {
      categories: undefined
    }
  },
  methods:{
  },
  beforeMount() {
  },
  computed:{
  }

}
</script>

<style scoped>

</style>
